from datetime import datetime as dt
# import json
"""
  if an app failes multipple times this alert is triggered.
"""

# --------------------------------------------------------------
timeWindow = {
            "delta" : 60,
            "indication" : { 3:["ORANGE","WARNING"],
                             5:["PINK","CRITICAL"],
                             8:["TOMATO","FATAL"]
                           }
             }
# timeWindow = json.load(open('timewindow.conf'))
# --------------------------------------------------------------
body = """ 
            <br><br>
            Hi team,
            <br>
            <b>Application "{appid}" have been failed multiple times</b>
            <br><br>
            <div>
              <table>
              <tbody>

                  <tr bgcolor="THISTLE">
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
                            <!-- COMMENTED <th style="padding-left:10px;padding-right:10px"><u>ports</u></th> -->
                            <!-- COMMENTED <th style="padding-left:10px;padding-right:10px"><u>version</u></th> -->
                            <!-- COMMENTED <th style="padding-left:10px;padding-right:10px"><u>slaveid</u></th> -->
                            <!-- COMMENTED <th style="padding-left:10px;padding-right:10px"><u>message</u></th> --> 
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


# ------------------------------------------------------------------------------------------------------
def getsubject(appid):
  return (
          '_alert_{stime} : {appid} - FAILED MULTIPLE TIMES'
              .format(stime=dt.utcnow().strftime('%Y-%m-%dT%H:%M:%S UTC'),appid=appid)
          )


def getbody(appid,AppStatusRecorder):

  fillups ={}

  lastxseconds = timeWindow['delta']
  eventlist = AppStatusRecorder.get_events_in_last_xseconds(appid,lastxseconds=lastxseconds)
  #                                   filter_predicate=lambda e: e.taskStatus in cls.TERMINAL_STATES)
  if not eventlist:
    print 'empty evenets in last %d seconds' % lastxseconds
    return None
  #checking timewindow size is enough.
  tailtohead =  abs(eventlist[0].timestamp - eventlist[-1].timestamp).seconds
  print 'timewindow = %d secs' % tailtohead
  # print "tailtohead",tailtohead
  if not tailtohead > lastxseconds * 0.8:
    return None

  rate = len(filter(lambda e: e.taskStatus in AppStatusRecorder.TERMINAL_STATES ,eventlist))

  print "RATE",rate

  indications = sorted(timeWindow['indication'].keys(),reverse=True)
  if rate < indications[-1]:  # minimum rate to address
    print "not enough failure to alert"
    return None

  for i in indications:
    if rate >= i:
       fillups['alertcolor'] = timeWindow['indication'][i][0]
       fillups['alertlevel'] = timeWindow['indication'][i][1]
       break

  fillups['ctime'] =  dt.utcnow().strftime('%c') + ' UTC'

  table_body = ""
  for ev in eventlist:
        rowstyle = 'style="background-color:INDIANRED"'   if ev.taskStatus in AppStatusRecorder.TERMINAL_STATES else ''
        table_body += """
                <tr {rowstyle}>
                  <td style="padding-left:10px;padding-right:10px" align="center">{timestamp}</td>
                  <td style="padding-left:10px;padding-right:10px" align="center">{taskStatus}</td>
                  <td style="padding-left:10px;padding-right:10px" align="center">{host}</td>
                  <!-- COMMENTED <td style="padding-left:10px;padding-right:10px" align="center">{ports}</td> -->
                  <!-- COMMENTED <td style="padding-left:10px;padding-right:10px" align="center">{version}</td> -->
                  <!-- COMMENTED <td style="padding-left:10px;padding-right:10px" align="center">{slaveId}</td> --> 
                  <!-- COMMENTED <td style="padding-left:10px;padding-right:10px" align="center">{message}</td> -->
                </tr>
                """.format(rowstyle=rowstyle,
                          timestamp=str(ev.timestamp),taskStatus=ev.taskStatus, host=ev.host,
                          ports=str(ev.ports), version=ev.version, slaveId=ev.slaveId,message=str(ev.message)
                    )

  fillups['appid'] = appid

  fillups['table_body'] = table_body

  return body.format(**fillups)