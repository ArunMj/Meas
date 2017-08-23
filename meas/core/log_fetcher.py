import requests
import os.path
from itertools import chain

# def get_marathon_info(host, port, url_pattern="http://{host}:{port}/v2/info", **request_params):
# marathon_url = "http://localhost:8080"
#     info_api = url_pattern.format(host=host, port=port)
#     return requests.get(info_api, **request_params).json()


def get_log_path(agent_host, agent_port, task_id, **request_params):
    mesos_agent_state_api_url = "http://{host}:{port}/state".format(host=agent_host, port=agent_port)
    resp = requests.get(mesos_agent_state_api_url, **request_params)
    if not resp.ok:
        print "** log fetcher: couldnt get log path of %s" % task_id, resp.content
        return
    state = resp.json()

    # generator which search marathon in active framework list. if not found search in completed_frameworks
    # yields all occurance of marathon frameworks.
    marathon_frameworks = chain((fw for fw in state['frameworks'] if fw['name'] == 'marathon'),
                                (fw for fw in state['completed_frameworks'] if fw['name'] == 'marathon'))

    for marathon_fw in marathon_frameworks:
        print '** log fetcher: marathon id=', marathon_fw['id']
        # search tasks in framework. (look into completed executor list first)
        # executor id is seems equal to the task id. No exceptions has found
        task_executor = (next((executor for executor in marathon_fw['completed_executors']
                               if executor['id'] == task_id), None) or
                         next((executor for executor in marathon_fw['executors']
                               if executor['id'] == task_id), None)
                         )
        if task_executor:
            return task_executor['directory']


def get_file_tail(agent_host, agent_port, filepath, size=10000, **request_params):
    """
    gets last n bytes of file content. default 10kb
    """
    fileread_api_url = "http://{host}:{port}/files/read".format(host=agent_host, port=agent_port)
    resp = requests.get(fileread_api_url, {'path': filepath, }, **request_params)
    if not resp.ok:
        print "** log fetcher:couldnt get tail of %s" % filepath, resp.content
        return
    last_offset = resp.json()['offset']
    offset = max(last_offset - size, 0)
    return requests.get(fileread_api_url,
                        {'path': filepath, 'offset': offset, 'length': size},
                        **request_params).json()['data']


def get_std_logs(task_id, agent_host='localhost', agent_port='5051'):
    stdout, stderr = None, None
    log_dir = get_log_path(agent_host, agent_port, task_id)
    if log_dir:
        stderr_file = os.path.join(log_dir, 'stderr')
        stdout_file = os.path.join(log_dir, 'stdout')
        stderr = get_file_tail(agent_host, agent_port, stderr_file)
        stdout = get_file_tail(agent_host, agent_port, stdout_file)
    return stdout, stderr


if __name__ == '__main__':
    # minfo = get_marathon_info('192.168.150.17', 8080, auth=('flyuser', 'flypassWORD'))
    # mesos_leader_ui_url = minfo['marathon_config']['mesos_leader_ui_url']
    # task_id = 'neon_apps_dk_ostrich-uploader.afe2ef76-8709-11e7-befb-001a4af92888'

    # frameworkId = minfo['frameworkId']
    # mesos-dns.fdf76ab5-83e1-11e7-a106-001a4af92888
    # fw: 165693b7-ff32-4df2-8987-98e799cec803-0001

    print get_std_logs('registry.f0c7814a-87e0-11e7-ba65-001a4af92888', '192.168.150.18')
