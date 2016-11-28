
"""
  if an app failes multipple times this alert is triggered.
"""

from datetime import datetime as dt
marathonhost = 'localhost'

def getsubject(**kwargs):
  """
    param1 : appid
  """
  appid = kwargs['appid']
  return (
    'marathon@'+ marathonhost+ '_'+  
      dt.utcnow().strftime('%Y-%m-%dT%H:%M:%S UTC:')
        + ' "'+appid+'"' + ' FAILED'
  )

def getbody(**kwargs):
  """
    param1 : appid
    param2:  eventlist
  """

  appid = kwargs['appid']
  eventlist = kwargs['eventlist']

  fillups ={}
  fillups['ctime'] =  dt.utcnow().strftime('%c') + ' UTC'
  table_body = ""
  for ev in eventlist:
        table_body += """
                <tr>
                  <td style="padding-left:10px;padding-right:10px" align="center">{timestamp}</td>
                  <td style="padding-left:10px;padding-right:10px" align="center">{taskStatus}</td>
                  <td style="padding-left:10px;padding-right:10px" align="center">{host}</td>
                  <td style="padding-left:10px;padding-right:10px" align="center">{ports}</td>
                  <td style="padding-left:10px;padding-right:10px" align="center">{version}</td>
                  <td style="padding-left:10px;padding-right:10px" align="center">{slaveId}</td>
                  <td style="padding-left:10px;padding-right:10px" align="center">{message}</td>
                </tr>
                """.format(timestamp=str(ev.timestamp),taskStatus=ev.taskStatus, host=ev.host,
                          ports=str(ev.ports), version=ev.version, slaveId=ev.slaveId,message=str(ev.message)
                    )
  fillups['appid'] = appid
  fillups['marathonhost'] = marathonhost
  fillups['alertcolor']="red"
  fillups['alertlevel']="CRITICAL"
  fillups['table_body'] = table_body
  return body.format(**fillups)



body = """ 
<br><br>
Hi team,
<br>
<b>Application "{appid}" have been failed at `{ctime}` on marathon@{marathonhost}</b>
<br><br>
<div>
  <table>
   <tbody>

      <tr bgcolor="yellow">
        <td align="left"><b>{ctime}</b></td>
        <td align="right"><b>{appid}</b></td>
      </tr>

      <tr>
        <td colspan="2"align="center"bgcolor="{alertcolor}"><b>{alertlevel}</b></td>
      </tr>

      <tr>
        <td colspan="2"align="center">Failure History<br>
          <table border="1" style= "border-collapse:collapse">
            <tbody>
              <tr>
                <th style="padding-left:10px;padding-right:10px"><u>timestamp</u></th>
                <th style="padding-left:10px;padding-right:10px"><u>taskStatus</u></th>
                <th style="padding-left:10px;padding-right:10px"><u>host</u></th>
                <th style="padding-left:10px;padding-right:10px"><u>ports</u></th>
                <th style="padding-left:10px;padding-right:10px"><u>version</u></th>
                <th style="padding-left:10px;padding-right:10px"><u>slaveid</u></th>
                <th style="padding-left:10px;padding-right:10px"><u>message</u></th>
              </tr>
              {table_body}
            </tbody>
          </table>
        </td>
      </tr>

   </tbody>
  </table>
</div>

</div><br></div>
"""


if __name__ == '__main__':
  print getsubject("/testapp")
  print getbody("/testapp",[])