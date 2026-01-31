EMAIL_LAYOUT = """
Hi All,<br><br>
Please find the Daily Monitoring Report<br><br>

<table border="1" cellpadding="6" cellspacing="0" width="100%"
 style="border-collapse:collapse;font-family:Calibri;font-size:13px;">

<tr>
  <td colspan="7" align="center" style="color:red;font-weight:bold;">
    Daily Monitoring Report
  </td>
</tr>

<tr>
  <td colspan="7" align="center">
    <b>Checklist Status - {{CHECKLIST_DATE}}</b>
  </td>
</tr>

<tr style="background:#9db7d8;font-weight:bold;">
<td>Sl. No.</td>
<td>Item Type</td>
<td>Item Name</td>
<td>Module</td>
<td>Case #</td>
<td>Status</td>
<td>Remarks</td>
</tr>

<!-- 1–3 LOGIN CHECK -->
<tr><td>1</td><td rowspan="3">Login Check</td><td>Windows Client Login</td><td rowspan="2">Admin Client</td><td></td><td>PASS</td><td>Working as expected.</td></tr>
<tr><td>2</td><td>Bizadmin Login</td><td></td><td>PASS</td><td>Working as expected.</td></tr>
<tr><td>3</td><td>Web Client Login</td><td>End User Client</td><td></td><td>PASS</td><td>Working as expected.</td></tr>

<!-- 4–6 WEB TAB CHECK -->
<tr><td>4</td><td rowspan="3">Web tab Check</td><td>Forms Builder Form Tab</td><td rowspan="2">Lead Form</td><td></td><td>PASS</td><td>Working as expected.</td></tr>
<tr><td>5</td><td>Create Lead using FB</td><td></td><td>PASS</td><td>Working as expected.</td></tr>
<tr><td>6</td><td>Cvue Activities Tab</td><td>CNS Activities</td><td></td><td>PASS</td><td>Working as expected.</td></tr>

<!-- 7–8 RFI -->
<tr><td>7</td><td rowspan="2">RFI Check</td><td>Post a Lead via query string</td><td rowspan="2">Lead Creation</td><td></td><td>PASS</td><td>Working as expected.</td></tr>
<tr><td>8</td><td>Check the RFI log file size</td><td></td><td>PASS</td><td></td></tr>

<!-- 9–30 CONNECTOR CHECK -->
<tr><td>9</td><td rowspan="22">Connector Check</td><td>Test login to CRM endpoint</td><td rowspan="4">Queue Manager</td><td></td><td>PASS</td><td></td></tr>
<tr><td>10</td><td>Test login to CNS endpoint</td><td></td><td>PASS</td><td></td></tr>
<tr><td>11</td><td>Send test message</td><td></td><td>PASS</td><td></td></tr>
<tr><td>12</td><td>Check all connector queues</td><td></td><td>PASS</td><td></td></tr>

<tr><td>13</td><td>C2K (live_100537) Create sisQueue Message for reference type table Job</td><td rowspan="4">Connector Jobs</td><td></td><td>PASS</td><td></td></tr>
<tr><td>14</td><td>C2K (live_100537) CRM Send Students Job</td><td></td><td>PASS</td><td></td></tr>
<tr><td>15</td><td>C2K (live_100537) Purge CmSisQueue Table Job</td><td></td><td>PASS</td><td></td></tr>
<tr><td>16</td><td>C2K (live_100537) Send Processed Message From CmSisQueue to CmSisQueueProcessed Job</td><td></td><td>PASS</td><td></td></tr>

<tr><td>17</td><td>Leads promoted in last 1 hour</td><td rowspan="5"></td><td></td><td>PASS</td><td>{{REMARK:Leads promoted in last 1 hour}}</td></tr>
<tr><td>18</td><td>Connector queue count - Pending</td><td></td><td>PASS</td><td>{{REMARK:Connector queue count - Pending}}</td></tr>
<tr><td>19</td><td>Connector queue count - Error</td><td></td><td>PASS</td><td>{{REMARK:Connector queue count - Error}}</td></tr>
<tr><td>20</td><td>Connector queue count - Successful</td><td></td><td>PASS</td><td>{{REMARK:Connector queue count - Successful}}</td></tr>
<tr><td>21</td><td>Last Lead promoted</td><td></td><td>PASS</td><td>{{REMARK:Last Lead promoted}}</td></tr>

<tr><td>22</td><td>Last Incoming from CNS</td><td rowspan="9">Connector - CNS to CRM</td><td></td><td>PASS</td><td>{{REMARK:Last Incoming from CNS}}</td></tr>
<tr><td>23</td><td>Connector queue count - Pending</td><td></td><td>PASS</td><td>{{REMARK:Connector queue count - Pending CNS}}</td></tr>
<tr><td>24</td><td>Connector queue count - Tagged</td><td></td><td>PASS</td><td>{{REMARK:Connector queue count - Tagged}}</td></tr>
<tr><td>25</td><td>Connector queue count - Error</td><td></td><td>PASS</td><td>{{REMARK:Connector queue count - Error CNS}}</td></tr>
<tr><td>26</td><td>Connector queue count - Successful</td><td></td><td>PASS</td><td>{{REMARK:Connector queue count - Successful CNS}}</td></tr>
<tr><td>27</td><td>Connector queue count - Discarded</td><td></td><td>PASS</td><td>{{REMARK:Connector queue count - Discarded}}</td></tr>
<tr><td>28</td><td>Processed in last two hours</td><td></td><td>PASS</td><td>{{REMARK:Processed in last two hours}}</td></tr>
<tr><td>29</td><td>Last successfully processed message</td><td></td><td>PASS</td><td>{{REMARK:Last successfully processed message}}</td></tr>
<tr><td>30</td><td>Pending in last six hours</td><td></td><td>PASS</td><td>{{REMARK:Pending in last six hours}}</td></tr>

<!-- 31–101 SYSTEM / JOB CHECKS -->
<tr><td>31</td><td>App Check</td><td>Application Server</td><td></td><td></td><td>PASS</td><td>Working as expected</td></tr>
<tr><td>32</td><td>DNC Log check</td><td>DNC Logs</td><td></td><td></td><td>PASS</td><td></td></tr>
<tr><td>33</td><td>RFI Logs</td><td>RFI Logs</td><td>RFI Logs(WEB15)</td><td></td><td>PASS</td><td>{{REMARK:RFI Logs}}</td></tr>

<tr>
  <td rowspan="2">34</td>
  <td rowspan="2">Archive</td>
  <td>Archiving of Attempt – tlMain</td>
  <td rowspan="2">Archive</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Archiving of Attempt – tlMain}}</td>
</tr>
<tr>
  <td>Archiving of Attempt – tlArchive</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Archiving of Attempt - tlArchive}}</td>
</tr>

<tr>
  <td rowspan="2">35</td>
  <td rowspan="2">Archive</td>
  <td>Archiving of Lead – tlMain</td>
  <td rowspan="2">Archive</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Archiving of Lead - tlMain}}</td>
</tr>
<tr>
  <td>Archiving of Lead – tlArchive</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Archiving of Lead - tlArchive}}</td>
</tr>

<tr>
  <td rowspan="2">36</td>
  <td rowspan="2">Archive</td>
  <td>Archiving of Interaction – tlMain</td>
  <td rowspan="2">Archive</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Archiving of Interaction - tlMain}}</td>
</tr>
<tr>
  <td>Archiving of Interaction – tlArchive</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Archiving of Interaction - tlArchive}}</td>
</tr>

<!-- 37–77 SQL CHECK -->
<tr>
  <td>37</td>
  <td rowspan="41">SQL Check</td>
  <td>Data and Log file size</td>
  <td rowspan="2">System Health</td>
  <td></td>
  <td>PASS</td>
  <td></td>
</tr>
<tr>
  <td>38</td>
  <td>Replication</td>
  <td></td>
  <td>PASS</td>
  <td></td>
</tr>

<tr>
  <td>39</td>
  <td>JSF job</td>
  <td>Emails</td>
  <td></td>
  <td>PASS</td>
  <td>Incoming and Outgoing emails are tested manually.</td>
</tr>

<tr>
  <td>40</td>
  <td>Campaign Dispatcher job</td>
  <td>Campaigns</td>
  <td></td>
  <td>PASS</td>
  <td>Sample Campaign ID : 001-414 is created and tested manually.</td>
</tr>

<tr>
  <td>41</td>
  <td>SQL Blocks & Deadlocks</td>
  <td>Performance</td>
  <td></td>
  <td>PASS</td>
  <td></td>
</tr>

<tr>
  <td>42</td>
  <td>Last Interaction</td>
  <td>Interactions</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Last Interaction}}</td>
</tr>

<tr>
  <td>43</td>
  <td>Last URL Clicked</td>
  <td>URL Clicks</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Last URL Clicked}}</td>
</tr>

<tr>
  <td>44</td>
  <td>Last Inquiry Lead created</td>
  <td>Lead Creation</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Last Inquiry Lead created}}</td>
</tr>

<tr>
  <td>45</td>
  <td>Last Application received</td>
  <td>Lead Creation</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Last Application received}}</td>
</tr>

<tr>
  <td>46</td>
  <td>Lead created in last 1 hour</td>
  <td>Lead Creation</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Lead created in last 1 hour}}</td>
</tr>

<tr>
  <td>47</td>
  <td>Last Attachment received</td>
  <td>Attachments</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Last Attachment received}}</td>
</tr>

<tr>
  <td>48</td>
  <td>Last one to one SMS</td>
  <td>SMS - one to one</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Last one to one SMS}}</td>
</tr>

<tr>
  <td>49</td>
  <td>Last SMS Campaign sent</td>
  <td>Campaigns</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Last SMS Campaign sent}}</td>
</tr>

<tr>
  <td>50</td>
  <td>Last Campaign Mailer Sent</td>
  <td>Campaigns</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Last Campaign Mailer Sent}}</td>
</tr>

<tr>
  <td>51</td>
  <td>Count Of Campaign Email sent</td>
  <td>Campaigns - Email</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Count Of Campaign Email sent}}</td>
</tr>

<tr>
  <td>52</td>
  <td>Count Of Campaign SMS sent</td>
  <td>Campaigns - Text</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Count Of Campaign SMS sent}}</td>
</tr>

<tr>
  <td>53</td>
  <td>Count of Attempts</td>
  <td>Phone Calls</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Count of Attempts}}</td>
</tr>

<tr>
  <td>54</td>
  <td>Count of one-to-one SMS sent</td>
  <td>SMS - one to one</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Count of one-to-one SMS sent}}</td>
</tr>

<tr>
  <td>55</td>
  <td>Count of Interactions</td>
  <td>Interactions</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Count of Interactions}}</td>
</tr>

<tr>
  <td>56</td>
  <td>Count of Leads</td>
  <td>Leads</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:Count of Leads}}</td>
</tr>

<tr>
  <td>57</td>
  <td>DNCImportStagingTable</td>
  <td>DNC</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:DNCImportStagingTable}}</td>
</tr>

<tr>
  <td>58</td>
  <td>DNCImportBatchNumbers</td>
  <td>DNC</td>
  <td></td>
  <td>PASS</td>
  <td>{{REMARK:DNCImportBatchNumbers}}</td>
</tr>

<tr>
  <td>59</td>
  <td>tblIncomingSkip table</td>
  <td rowspan="2">Emails</td>
  <td></td>
  <td>CHECKED</td>
  <td>No emails observed</td>
</tr>

<tr>
  <td>60</td>
  <td>No. of emails stuck in Outbox</td>
  <td></td>
  <td>PASS</td>
  <td>No emails observed</td>
</tr>

<tr>
  <td>61</td>
  <td>SQL Server log</td>
  <td></td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>62</td>
  <td>CRM SQL Jobs</td>
  <td>CRM SQL Job health</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>63</td>
  <td>Retention Import Job</td>
  <td>Advising Data</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>64</td>
  <td>Financial Aid Import Job</td>
  <td>Financial Aid Data</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>65</td>
  <td>Gravity to CRM Attachment Import Job</td>
  <td>Applications</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>66</td>
  <td>CRM to CNS Document Update Job</td>
  <td>Document Status</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>67</td>
  <td>DNC Delta Import Job</td>
  <td>DNC</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>68</td>
  <td>DNC Update Job</td>
  <td>DNC</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>69</td>
  <td>TPS - Update Current LDA on Contact</td>
  <td>DNC</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>70</td>
  <td>TPS - Update FDNC Status - 30 Day Recycle</td>
  <td>DNC</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>71</td>
  <td>TPS - DNC Scrub - 30 Day Recycle</td>
  <td>DNC</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>72</td>
  <td>Update Financial Aid Hold Job</td>
  <td>Financial Aid Data</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>73</td>
  <td>Update Lead Source Category Job</td>
  <td>Marketing</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>74</td>
  <td>Update Cancel Status Reason Job</td>
  <td>Admissions Data</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>75</td>
  <td>Document Status Import Job</td>
  <td>Document Status</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>76</td>
  <td>Update 60 Day Property Job</td>
  <td>Lead Creation</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>77</td>
  <td>Attempt Import Job</td>
  <td>Phone Calls</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>


<tr><td>78</td><td>Analytics Check</td><td>Scheduled Reports</td><td>Reports</td><td></td><td>PASS</td><td>Working as expected</td></tr>
<tr>
  <td>79</td>
  <td rowspan="13">Service Check</td>
  <td>TLScheduledReportService</td>
  <td>Schedule report (WEB14)</td>
  <td></td>
  <td>PASS</td>
  <td></td>
</tr>

<tr>
  <td>80</td>
  <td>tlMail Service (Extractor)</td>
  <td>Emails (WEB14)</td>
  <td></td>
  <td>PASS</td>
  <td>Incoming and Outgoing emails are tested manually.</td>
</tr>

<tr>
  <td>81</td>
  <td>tlMail Service (Dispatcher)</td>
  <td>Emails (WEB14)</td>
  <td></td>
  <td>PASS</td>
  <td>Incoming and Outgoing emails are tested manually.</td>
</tr>

<tr>
  <td>82</td>
  <td>Campaign Dispatcher - Email</td>
  <td>Campaigns (WEB14)</td>
  <td></td>
  <td>PASS</td>
  <td>Sample Campaign ID : 001-414 is created and tested manually.</td>
</tr>

<tr>
  <td>83</td>
  <td>WebNotification service</td>
  <td>Phone Calls (WEB13)</td>
  <td></td>
  <td>PASS</td>
  <td>Notifications/Broadcast Successful.</td>
</tr>

<tr>
  <td>84</td>
  <td>SMS Dispatcher (3)</td>
  <td>Texting - one to one (WEB18)</td>
  <td></td>
  <td>PASS</td>
  <td>SMS received successfully.</td>
</tr>

<tr>
  <td>85</td>
  <td>SMSDispatcherServiceCustom (True dialog)</td>
  <td>Texting - one to one (WEB18)</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>86</td>
  <td>Call campaign extract service</td>
  <td>Call Campaigns (WEB17)</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>87</td>
  <td>Connector service</td>
  <td>Lead Promotion</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>88</td>
  <td>RemoveLeadFromDialer.Service</td>
  <td>Integration (WEB17)</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>89</td>
  <td>Transmit Service</td>
  <td>Transmit Tracker (WEB13)</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>90</td>
  <td>Campaign Dispatcher - SMS</td>
  <td>Campaigns (WEB18)</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>91</td>
  <td>SMS Extractor (3)</td>
  <td>Texting - one to one (WEB18)</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<!-- 92 ARCHIVE (MERGED) -->
<tr>
  <td rowspan="2">92</td>
  <td rowspan="2">Archive</td>
  <td>Archiving of Campaign - tlMain</td>
  <td rowspan="2">Archive</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>
<tr>
  <td>Archiving of Campaign - tlArchive</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<!-- 93 SPACE CHECK -->
<tr>
  <td>93</td>
  <td>Space Check</td>
  <td>Server Disk Space</td>
  <td>System Health</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<!-- 94 EVENT VIEWER - DB SERVER -->
<tr>
  <td>94</td>
  <td>Event Viewer Check<br>DB Server</td>
  <td>Event Logs</td>
  <td></td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<!-- 95 EVENT VIEWER - APP SERVER -->
<tr>
  <td>95</td>
  <td>Event Viewer Check<br>App Server</td>
  <td>Event Logs</td>
  <td></td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<!-- 96 EVENT VIEWER - WEB SERVER -->
<tr>
  <td>96</td>
  <td>Event Viewer Check<br>Web Server</td>
  <td>Event Logs</td>
  <td></td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>97</td>
  <td rowspan="3">Task Check</td>
  <td>GravityFormsSFTPTransfer_TEST</td>
  <td>Call Campaigns (NFS1)</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>98</td>
  <td>TPSFileMover</td>
  <td>Applications (WEB17)</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<tr>
  <td>99</td>
  <td>DNC Service</td>
  <td>DNC (WEB15)</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<!-- 100 IIS APP POOL -->
<tr>
  <td>100</td>
  <td>IIS App Pool Check</td>
  <td>IIS App Pool health check</td>
  <td>Web Apps</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

<!-- 101 APPLICATION INSIGHTS -->
<tr>
  <td>101</td>
  <td>Application Insights</td>
  <td>Check Application Insight to Ensure Workflows are Working Correctly</td>
  <td>Application Insights</td>
  <td></td>
  <td>-</td>
  <td>Not executed</td>
</tr>

</table>

<br><br>
<b>Additional Checks</b><br><br>

<table border="1" cellpadding="6" cellspacing="0" width="60%"
 style="border-collapse:collapse;font-family:Calibri;font-size:13px;">

<tr style="background:#9db7d8;font-weight:bold;">
  <td>Sl. No.</td>
  <td>Item Name</td>
  <td>Case #</td>
  <td>Status</td>
  <td>Remarks</td>
</tr>

<tr>
  <td>1</td>
  <td>Leads Posting</td>
  <td></td>
  <td>PASS</td>
  <td></td>
</tr>

<tr>
  <td>2</td>
  <td>Outgoing Queue Processing</td>
  <td></td>
  <td>PASS</td>
  <td></td>
</tr>

<tr>
  <td>3</td>
  <td>Incoming Queue Processing</td>
  <td></td>
  <td>PASS</td>
  <td></td>
</tr>

<tr>
  <td>4</td>
  <td>Notifications/Broadcast Successful</td>
  <td></td>
  <td>PASS</td>
  <td></td>
</tr>

<tr>
  <td>5</td>
  <td>Phone Session Screenpop Successful</td>
  <td></td>
  <td>PASS</td>
  <td></td>
</tr>

<tr>
  <td>6</td>
  <td>Manual Internal email test – Incoming & Outgoing</td>
  <td></td>
  <td>PASS</td>
  <td></td>
</tr>

<tr>
  <td>7</td>
  <td>Manual External email test – Incoming & Outgoing</td>
  <td></td>
  <td>PASS</td>
  <td></td>
</tr>

</table>

<br>
Thanks,<br>
Manasa
"""
