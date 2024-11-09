from bs4 import BeautifulSoup

html_content = '''<body class="vsc-initialized">
<script type="text/javascript">
 $(document).ready(function(){
	 
    $(":submit").click(function() {
        $('#waitspinner').show();
    });
    
	$("a").click( function() {
        var id=$(this).attr('id');
        
        if (typeof id == "undefined") {
		   $('#waitspinner').show(); 
        }  
		else if(id!=='download' && id.indexOf("help")!=0 )
		{
		   $('#waitspinner').show(); 
        }
	});

     $("table[id^=sortableTable").tablesorter({
   	  theme: 'drexel',
   	  cssInfoBlock : "totals-no-sort", 
    	  widgets: ['zebra', 'stickyHeaders']
	  });
  });
 </script>

<table width="100%" cellspacing="0" cellpadding="1">


<!-- Begin Header Image -->
<tbody><tr><td>
<table width="100%" border="0" cellspacing="0" cellpadding="0">
	<tbody><tr>
	  <td valign="top">
		<div id="header">
			<div id="logo-container">
			<a href="http://drexel.edu/"><img src="/webtms_du/images/logo-drexel.png" alt="Drexel University" height="134" width="126"></a>
			<h2 id="bar">Term Master Schedule</h2>
			</div>
			<div id="logoutlink">    
			<span> <a href="/webtms_du/logout"> Logout</a></span>
			</div>
		</div>
	   </td>
	 </tr>
</tbody></table>
</td></tr>	
<!-- End Header Image -->

<!-- Begin body content, which is unique to each page -->
<tr><td>


<!-- Begin breadcrumb -->
<table id="breadcrumb" cellspacing="0" cellpadding="0" width="100%">
	<tbody><tr>
		<td>
			<ul id="breadcrumbTrail">
			<li class="first"><a href="http://www.drexel.edu">Drexel Home</a></li>
			<li><a href="/webtms_du/">WebTMS Home / Terms</a></li>
			<li class="last"><span>Colleges / Subjects</span></li>
			</ul>
		</td>
		<td align="right"><b>Last Updated: November 8, 09:00 pm </b></td>
	</tr>
</tbody></table>
<!-- End breadcrumb -->


<!-- Begin main body -->
<table align="center" valign="top" bgcolor="#ffffff" border="0" cellpadding="0" cellspacing="0" width="100%">
	<tbody><tr>
		<td>&nbsp;</td>
	</tr>

	<tr>
		<td colspan="3" width="800" class="title"><div align="left">Schedule for Fall Quarter 24-25 (202415)</div></td>
	</tr>
	 
   
	  
	  
	<tr>	
		<td valign="top">
		  <div id="sideLeft"><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=A">Antoinette Westphal COMAD</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=AS">Arts and Sciences</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=B">Bennett S. LeBow Coll. of Bus.</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=CV">Center for Civic Engagement</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=C">Close Sch of Entrepreneurship</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=CI">Col of Computing &amp; Informatics</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=E">College of Engineering</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=PH">Dornsife Sch of Public Health</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=GC">Goodwin Coll of Prof Studies</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=X">Miscellaneous</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=NH">Nursing &amp; Health Professions</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=PE">Pennoni Honors College</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=R">Sch.of Biomed Engr,Sci &amp; Hlth</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=T">School of Education</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"><a href="/webtms_du/collegesSubjects/202415?collCode=L">Thomas R. Kline School of Law</a><img src="/webtms_du/images/nav_divider.gif" alt="" width="250" height="2"></div>
		</td>

		<td align="left" valign="top">
			<table>
			
							
				<tbody><tr>
					<td colspan="1" class="sectionText">For courses specific to a college/school, select the college from the left navigation menu, and then select the subject.</td>
				</tr>
				<tr>
					<td>
					<table class="collegePanel" border="0">

						<tbody><tr><td align="center" class="boxHeader">Subjects of Antoinette Westphal COMAD</td></tr>
						
						<tr>
							<td>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/ANIM">Animation (ANIM)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/ARCH">Architecture (ARCH)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/ARTH">Art History (ARTH)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/AAML">Arts Admin &amp; Museum Leadership (AAML)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/AADM">Arts Administration (AADM)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/DANC">Dance (DANC)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/DSMR">Design &amp; Merchandising (DSMR)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/DSRE">Design Research (DSRE)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/DIGM">Digital Media (DIGM)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/EAM">Entertainment &amp; Arts Managemnt (EAM)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/FASH">Fashion Design (FASH)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/FMTV">Film &amp; TV Production (FMTV)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/FMST">Film Studies (FMST)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/GMAP">Game Art and Production (GMAP)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/VSCM">Graphic Design (VSCM)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/IDM">Interactive Digital Media (IDM)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/INTR">Interior Design (INTR)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/MUSL">Museum Leadership (MUSL)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/MUSC">Music (MUSC)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/MIP">Music Industry Program (MIP)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/PRFA">Performing Arts (PRFA)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/PHTO">Photography (PHTO)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/PROD">Product Design (PROD)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/RMER">Retail &amp; Merchandising (RMER)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/SCRP">Screenwriting &amp; Playwriting (SCRP)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/TVST">TV Studies (TVST)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/TVMN">Television Management (TVMN)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/THTR">Theatre (THTR)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/URBS">Urban Strategy (URBS)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/VRIM">VR and Immersive Media Design (VRIM)</a></div>
							  
							  <div class="odd"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/VSST">Visual Studies (VSST)</a></div>
							  
							  <div class="even"><img src="/webtms_du/images/arrow-orange-small.gif" border="0" alt="" width="10" height="8">&nbsp;&nbsp;<a href="/webtms_du/courseList/WEST">WEST Studies (WEST)</a></div>
							  
							</td>
						</tr>
						

					</tbody></table>
					</td>
				</tr>
			</tbody></table>
		</td>
	</tr>
    
   	

	<tr>
			<td>&nbsp;</td>
	</tr>
 		
</tbody></table>
<!-- End main body -->

	</td></tr>
<!-- End body content body -->

<!-- Begin footer HTML code segment  -->
<tr><td>
<table width="100%">
	<tbody><tr>
	<td>
		<div id="footer">
			<div id="address">
				<p>Drexel University, 3141 Chestnut Street, Philadelphia, PA 19104,
				<a href="tel:2158952000">215.895.2000</a>, © All Rights Reserved.</p>
			</div>
		</div>
	</td>
	</tr>

	<tr>
	  <td height="15"><img src="/webtms_du/images/empty.gif" width="1" height="15"></td>
	</tr>
	<tr>
	  <td height="5"><img src="/webtms_du/images/empty.gif" width="1" height="5"></td>
	</tr>
</tbody></table>
</td></tr>
<!-- end footer HTML code segment  -->

</tbody></table>	
	

</body>'''  # Place your HTML content here as a string

soup = BeautifulSoup(html_content, 'html.parser')

# Find all divs with class 'odd' or 'even'
links = []
for div in soup.find_all(class_=["odd", "even"]):
    link = div.find('a')
    if link and link.get('href'):
        links.append(f"https://termmasterschedule.drexel.edu{link['href']}")

# Print all extracted links
for href in links:
    print(href)
