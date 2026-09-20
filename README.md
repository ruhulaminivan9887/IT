COMPLETE	BUILD	GUIDE	·	BEGINNER	FRIENDLY
End-to-End	AI-Driven
Security	Monitoring
Pipeline
Wazuh	SIEM	+	Windows	Agent	+	Ubuntu	Manager	+
Python	+	OpenAI
Built	from	absolute	scratch,	with	every	command,	every
mistake,	and	every	fix.
VirtualBox		•		Ubuntu	Linux		•		Windows		•		Wazuh	4.x		•		Python	3		•		OpenAI	API
Table	of	Contents
1.	What	You	Are	Building	(Plain-English	Overview)
2.	Before	You	Start	—	Requirements	Checklist
3.	Your	Lab	Network	Plan
4.	Phase	1	—	Install	VirtualBox	&	Create	Your	Two	Virtual	Machines
5.	Phase	2	—	Fix	the	Network	Mode	First	(Avoid	the	#1	Mistake)
6.	Phase	3	—	Install	the	Wazuh	Manager	on	Ubuntu
7.	Phase	4	—	Open	the	Firewall	Ports
8.	Phase	5	—	Set	Up	Easy	Copy-Paste	With	SSH
9.	Phase	6	—	Find	Your	Windows	Machine's	Real	IP	Address
10.	Phase	7	—	Register	the	Windows	Agent
11.	Phase	8	—	Install	the	Agent	on	Windows
12.	Phase	9	—	Verify	the	Agent	Shows	"Active"
13.	Phase	10	—	Write	the	Python	Log-Reader	Script
14.	Phase	11	—	Add	the	AI	Brain	(OpenAI	Integration)
15.	Phase	12	—	Test	the	Whole	Pipeline	End-to-End
16.	Full	Troubleshooting	Ledger	—	Every	Error	We	Hit	&	How	We	Fixed	It
17.	Optimization	&	Security	Hardening	Checklist
18.	What	This	Project	Proves	You	Can	Do
19.	Appendix	A	—	Full	Final	Scripts	(Copy-Paste	Ready)
20.	Appendix	B	—	One-Page	Command	Cheat	Sheet
1.	What	You	Are	Building	(Plain-English	Overview)
You	are	going	to	build	a	small,	working	security	operations	center	(SOC)	—	the	same	kind	of	setup	real	companies	use,	just	shrunk	down	to	fit	on
one	laptop	using	free	virtual	machines.
In	plain	words:	one	computer	(Ubuntu)	will	act	as	the	"security	guard's	office."	A	second	computer	(Windows)	will	act	as	the	"building	being
watched."	The	Windows	machine	will	constantly	report	what's	happening	on	it	(logins,	logoffs,	changes)	to	the	Ubuntu	machine.	Then,	a	small	Python
program	you	write	will	watch	those	reports	live	and	—	for	anything	that	looks	serious	—	ask	an	AI	(OpenAI)	to	explain	what	it	means	and	what	to	do
about	it,	in	plain	English.
	[	WINDOWS	MACHINE	]																					[	UBUNTU	MACHINE	]
	"the	thing	being	watched"															"the	security	office"
	---------------------------													--------------------------------------------
	Wazuh	AGENT	installed										---->				Wazuh	MANAGER	(receives	+	stores	events)
	sends:	logins,	logoffs,																							|
	file	changes,	system	events																			v
																																									alerts.json		(live	event	stream,	newest	at	bottom)
																																																|
																																																v
																																									your	Python	script	(wazuh_ai_parser.py)
																																									reads	each	new	alert	as	it	arrives
																																																|
																																					is	it	serious	(high	severity)?
																																							/																								\
																																			NO																												YES
																																				|																														|
																													print	routine	note										send	to	OpenAI	API
																																																										get	back	a	plain-English
																																																										threat	explanation
Why	this	matters:	this	exact	pattern	—	collect	logs	→	centralize	them	→	filter	them	→	let	AI	explain	the	important	ones	—	is	literally	what	SIEM	+	SOAR
tools	do	in	real	jobs.	You	are	building	a	mini	version	of	a	Splunk/Sentinel/Wazuh-plus-AI	pipeline.
2.	Before	You	Start	—	Requirements	Checklist
What	you	need
A	computer	with	at	least	8	GB	RAM	(16	GB	is
more	comfortable)
VirtualBox	(free)
An	Ubuntu	Server	or	Desktop	ISO	(22.04	or
newer)
A	Windows	ISO	(Windows	10/11,	or	Windows
Server	2019/2022)
Internet	connection	on	both	VMs
An	OpenAI	account	with	a	small	amount	of
credit	($5	is	plenty	to	test)
Patience	with	copy-pasting	commands	exactly
as	written
Notes
You'll	run	two	virtual	machines	at	once
Download	from	virtualbox.org
This	becomes	your	Wazuh	Manager
This	becomes	the	"watched"	machine,	your	Wazuh	Agent
Needed	to	download	Wazuh	and	to	reach	OpenAI's	servers
platform.openai.com	→	Billing
One	misplaced	character	breaks	Linux/Python	—	that's	normal,	not	a	sign	you	did	something	wrong
You	do	NOT	need	to	know	how	to	code.	Every	piece	of	code	in	this	guide	is	complete	and	ready	to	paste.	You	are	typing/pasting	commands,	not	writing
software	from	scratch.
3.	Your	Lab	Network	Plan
Write	down	your	own	IP	addresses	before	you	start	—	they	will	almost	certainly	be	different	from	the	example	ones	below	(that	mismatch	was	the
single	biggest	time-waster	in	the	original	build	of	this	project,	see	the	Troubleshooting	Ledger).
Role
Ubuntu	VM	—	Wazuh	Manager
Windows	VM	—	Wazuh	Agent
Example	IP	used	in	this	guide
192.168.0.111
192.168.0.142
Your	actual	IP	(fill	in)
______________
______________
Rule	of	thumb:	whatever	IP	you	write	down	for	the	Windows	machine,	get	it	by	running	
ipconfig	ON	that	Windows	machine	itself	—	never	guess	it,	never
assume	it.	This	single	habit	prevents	the	most	common	failure	in	this	whole	project.
4.	Phase	1	—	Install	VirtualBox	&	Create	Your	Two	Virtual	Machines
Step	1.1	—	Install	VirtualBox
1 Download	VirtualBox	from	virtualbox.org	for	your	operating	system	and	install	it	normally	(Next	→	Next	→	Install).
Step	1.2	—	Create	the	Ubuntu	VM	(this	becomes	your	Wazuh	Manager)
1.	Open	VirtualBox	→	click	New.
2.	Name	it	
Wazuh-Manager ,	type	=	Linux,	version	=	Ubuntu	(64-bit).
3.	Give	it	at	least	4	GB	RAM	and	40	GB	disk	(Wazuh's	indexer	is	memory-hungry).
4.	Attach	your	Ubuntu	ISO	and	finish	the	install	wizard	as	normal	(username,	password,	"install	OpenSSH	server"	if	it's	offered	here	—	say	yes,	it
saves	you	a	step	later).
Step	1.3	—	Create	the	Windows	VM	(this	becomes	your	Wazuh	Agent)
1.	Click	New	again	→	name	it	
Windows-Agent ,	type	=	Windows.
2.	Give	it	at	least	4	GB	RAM	and	50	GB	disk.
3.	Attach	your	Windows	ISO	and	finish	the	normal	Windows	setup	(create	a	local	account,	skip	Microsoft	account	if	you	want	simplicity).
5.	Phase	2	—	Fix	the	Network	Mode	First	(Avoid	the	#1	Mistake)
This	step	was	skipped	in	the	original	build	and	caused	most	of	the	connection	headaches	later	(see	Troubleshooting	Ledger,	rows	3	&	5).
Do	it	now,	before	installing	anything	else.
Two	VMs	on	VirtualBox's	default	"NAT"	network	mode	cannot	see	each	other	—	they	can	only	see	the	internet.	You	need	a	mode	where	they	can
talk	to	each	other	directly.
1.	Shut	down	both	VMs	if	they're	running.
2.	For	each	VM:	select	it	in	VirtualBox	→	Settings	→	Network.
3.	Set	Attached	to:	
Bridged	Adapter	(simplest	—	puts	both	VMs	on	your	real	home	network,	so	they	get	normal	IPs	like	192.168.0.x).	If	you	don't
want	them	on	your	home	network,	use	
Host-only	Adapter	on	both	instead	—	either	works	as	long	as	both	VMs	use	the	same	mode.
4.	Boot	both	VMs	back	up.
Also	turn	on	the	shared	clipboard	now	(VirtualBox	window	→	Devices	→	Shared	Clipboard	→	Bidirectional,	and	the	same	for	Drag	and	Drop).	It's
flaky	on	some	hosts	(see	Ledger	row	4)	which	is	exactly	why	Phase	5	sets	up	SSH	as	a	reliable	backup.
6.	Phase	3	—	Install	the	Wazuh	Manager	on	Ubuntu
RUN	THIS	ON:	Ubuntu	VM	terminal
Wazuh	publishes	one	official	script	that	installs	the	manager,	the	indexer,	and	the	dashboard	together.	Open	a	terminal	on	the	Ubuntu	VM	and	run:
curl	-sO	https://packages.wazuh.com/4.x/wazuh-install.sh
sudo	bash	./wazuh-install.sh	-a
This	takes	several	minutes.	When	it	finishes,	it	prints	the	dashboard	URL	and	an	auto-generated	
somewhere	safe	right	now,	it	is	only	shown	once.
admin	password	—	copy	that	password	down
Security	note:	change	this	password	the	first	time	you	log	in	(Dashboard	→	top-right	user	icon	→	profile).	Never	leave	the	auto-generated	one	in	place	long
term,	and	never	paste	it	into	a	chat,	email,	or	document	you	plan	to	share.
Confirm	your	Ubuntu	machine's	own	IP	address	(you'll	need	it	constantly):
ip	a
Look	for	
inet	192.168.x.x	under	your	main	network	adapter	—	that	is	your	Wazuh	Manager's	IP.	Write	it	in	the	table	in	Section	3.
Once	installed,	open	a	browser	(on	either	machine)	and	go	to	
https://<your-ubuntu-ip> .	You'll	get	a	certificate	warning	because	Wazuh	uses	a	self
signed	certificate	for	your	lab	—	click	Advanced	→	Proceed.	Log	in	with	
admin	and	the	password	you	saved.
7.	Phase	4	—	Open	the	Firewall	Ports
RUN	THIS	ON:	Ubuntu	VM	terminal
Wazuh	agents	talk	to	the	manager	over	TCP	ports	1514	(event	data)	and	1515	(agent	registration).	Open	both	now,	before	you	even	try	to	connect
an	agent:
sudo	ufw	allow	1514/tcp
sudo	ufw	allow	1515/tcp
sudo	ufw	reload
Double-check	the	manager	is	actually	listening	on	that	port:
sudo	ss	-tulpn	|	grep	1514
You	should	see	a	line	mentioning	
wazuh	and	
1514 .	If	you	see	nothing,	the	manager	service	isn't	fully	up	yet	—	wait	a	minute	and	try	again.
8.	Phase	5	—	Set	Up	Easy	Copy-Paste	With	SSH
RUN	THIS	ON:	Ubuntu	VM	terminal
Typing	long	Python	scripts	by	hand	into	a	VM	window	is	how	tiny	invisible	mistakes	creep	in	(see	Ledger	row	1).	SSH	lets	you	paste	code	straight	from	your
host	computer's	browser	into	a	normal	terminal	window	—	far	more	reliable	than	the	VirtualBox	clipboard.
Install	and	start	the	SSH	server	on	Ubuntu:
sudo	apt	update	&&	sudo	apt	install	openssh-server	-y
sudo	systemctl	enable	--now	ssh
RUN	THIS	ON:	your	physical	Windows	host	(NOT	inside	a	VM	window)	—	open	a	normal	PowerShell	window
ssh	yourusername@192.168.0.111
(replace	
yourusername	with	the	Ubuntu	account	you	created,	and	the	IP	with	your	own	Ubuntu	IP	from	Phase	3).	Type	
yes	if	asked	to	trust	the	host
fingerprint,	then	enter	your	Ubuntu	password.	You	are	now	inside	the	Ubuntu	machine,	but	typing/pasting	from	a	normal	Windows	terminal	—	copy
and	paste	(Ctrl+V,	or	right-click)	now	works	perfectly	for	every	command	in	the	rest	of	this	guide.
9.	Phase	6	—	Find	Your	Windows	Machine's	Real	IP	Address
RUN	THIS	ON:	Windows	VM,	PowerShell
ipconfig
Look	for	IPv4	Address	under	your	active	adapter	(usually	"Ethernet").	Write	this	exact	number	in	your	Section	3	table.	Do	not	guess	or	reuse	an
IP	from	an	example	—	this	was	the	single	biggest	source	of	wasted	time	in	the	original	build	(the	agent	was	registered	with	one	IP	while	the
machine	actually	had	a	different	one,	so	it	could	never	connect).
10.	Phase	7	—	Register	the	Windows	Agent
There	are	two	ways	to	do	this.	Method	A	(the	dashboard	wizard)	is	easier	and	recommended.	Method	B	(manual	CLI)	is	included	because	it's
useful	to	understand	and	is	a	good	fallback	if	the	wizard	misbehaves.
Method	A	—	Dashboard	Wizard	(recommended)
RUN	THIS	ON:	Wazuh	Dashboard,	in	your	browser
1.	Log	into	the	dashboard	→	menu	(three	lines,	top-left)	→	Agents	management	→	Summary	→	click	Deploy	new	agent.
2.	Operating	system:	Windows.
3.	Wazuh	server	address:	your	Ubuntu	IP	(e.g.	
192.168.0.111 ).
4.	Give	it	a	clear	name,	e.g.	
Windows-Agent .
5.	The	wizard	generates	a	ready-to-run	PowerShell	command	at	the	bottom	of	the	page	—	copy	it.	It	already	contains	the	correct	manager	address
and	a	registration	key	baked	in,	so	there's	no	separate	"extract	the	key"	step	with	this	method.
Method	B	—	Manual	CLI	Registration	(alternate	/	for	understanding)
RUN	THIS	ON:	Ubuntu	VM	terminal	(or	your	SSH	session)
sudo	/var/ossec/bin/manage_agents
Type	A	to	add	an	agent.
Agent	name:	e.g.	
Windows-Agent
Agent	IP:	the	exact	IP	you	found	in	Phase	6
Confirm	with	y	—	it	will	print	a	new	numeric	ID	(e.g.	
Now	extract	the	authentication	key	for	that	ID:
sudo	/var/ossec/bin/manage_agents
001 ).
Type	
E	to	extract	a	key,	enter	the	agent	ID,	and	copy	the	long	base64-looking	string	it	prints.	You'll	paste	this	into	PowerShell	in	the	next	phase.
R ,	enter	the	agent	ID	to	delete	it,	then	repeat	the	
If	you	ever	registered	an	agent	with	the	wrong	IP	(this	happened	in	the	original	build),	don't	try	to	edit	it	—	it's	faster	to	remove	and	re-add:	run
manage_agents ,	type	
A	steps	above	with	the	correct	IP.
11.	Phase	8	—	Install	the	Agent	on	Windows
RUN	THIS	ON:	Windows	VM	—	PowerShell,	opened	as	Administrator
Important:	this	must	be	PowerShell,	not	the	older	Command	Prompt	(cmd.exe).	If	a	command	below	gives	an	error	like	"is	not	recognized	as	the	name	of	a
cmdlet",	you	are	almost	certainly	in	Command	Prompt	by	mistake	—	close	it,	search	"PowerShell"	in	the	Start	Menu,	right-click	it,	and	choose	Run	as
Administrator.
If	you	used	Method	A	(dashboard	wizard):
Paste	the	exact	command	block	the	dashboard	generated	for	you.	It	looks	like	this	(yours	will	have	your	own	IP/name	baked	in):
Invoke-WebRequest	-Uri	https://packages.wazuh.com/4.x/windows/wazuh-agent-4.14.7-1.msi	-OutFile	$env:temp\wazuh-agent;	msiexec.exe	/i	
$env:temp\wazuh-agent	/q	WAZUH_MANAGER='192.168.0.111'	WAZUH_AGENT_NAME='Windows-Agent'
Then	start	the	service:
Start-Service	wazuh
If	you	used	Method	B	(manual	CLI	key):
Invoke-WebRequest	-Uri	https://packages.wazuh.com/4.x/windows/wazuh-agent-4.14.7-1.msi	-OutFile	wazuh-agent.msi
msiexec.exe	/i	wazuh-agent.msi	/qn	WAZUH_MANAGER='192.168.0.111'	WAZUH_AGENT_NAME='Windows-Agent'
Then	register	the	key	you	copied	in	Phase	7	and	start	the	service:
$key	=	"PASTE_YOUR_LONG_KEY_STRING_HERE"
Set-Content	-Path	"C:\Program	Files	(x86)\ossec-agent\client.keys"	-Value	$key
Start-Service	wazuh
12.	Phase	9	—	Verify	the	Agent	Shows	"Active"
RUN	THIS	ON:	Ubuntu	VM	(or	SSH	session)
sudo	/var/ossec/bin/agent_control	-l
You	want	to	see	your	agent	listed	with	status	Active.	You	can	double	check	visually	too:
Wazuh	Dashboard
Menu	→	Agents	management	→	Summary	(this	is	the	correct	page	—	note	there	is	also	a	separate	Groups	page	in	the	same	section	which	does
not	show	connection	status,	don't	confuse	the	two).	Your	agent's	status	column	should	read	Active	with	a	green	dot.
If	it	says	"Never	connected"	after	a	minute:	on	the	Windows	VM,	run	
Get-Service	wazuh	in	PowerShell	to	confirm	the	service	is	running,	then
Restart-Service	wazuh .	If	it's	still	stuck,	jump	to	row	6	of	the	Troubleshooting	Ledger	(the	port-1514	connectivity	test)	—	that	fixes	it	in	the	vast	majority
of	cases.
13.	Phase	10	—	Write	the	Python	Log-Reader	Script
RUN	THIS	ON:	Ubuntu	VM	(via	your	SSH	session,	so	you	can	paste)
Wazuh	writes	every	alert	it	receives,	in	real	time,	as	one	JSON	object	per	line,	to	this	file:
/var/ossec/logs/alerts/alerts.json
Note	the	path	has	an	alerts	folder	before	the	file	—	in	older	guides	you	may	see	/var/ossec/logs/alerts.json	with	no	folder,	which	is	wrong	for
current	Wazuh	4.x	versions	and	will	throw	FileNotFoundError	(Ledger	row	2).
Create	the	script	file	using	this	exact	command	block	(it	writes	the	whole	file	for	you	—	no	manual	typing,	no	indentation	mistakes):
cat	<<	'EOF'	>	wazuh_ai_parser.py
import	json
import	time
LOG_PATH	=	"/var/ossec/logs/alerts/alerts.json"
AGENT_NAME	=	"Windows-Agent"			#	<--	must	exactly	match	the	name	you	registered
def	monitor_logs():
				print(f"[*]	Listening	for	live	security	logs	from	{AGENT_NAME}	...")
				try:
								with	open(LOG_PATH,	"r")	as	f:
												f.seek(0,	2)		#	jump	to	the	end	so	we	only	see	NEW	alerts	from	now	on
												while	True:
																line	=	f.readline()
																if	not	line:
																				time.sleep(0.5)
																				continue
																try:
																				alert	=	json.loads(line)
																				if	alert.get("agent",	{}).get("name")	==	AGENT_NAME:
																								rule	=	alert.get("rule",	{})
																								level	=	rule.get("level",	0)
																								desc	=	rule.get("description",	"No	description")
																								print(f"\n[ALERT]	Level:	{level}	|	{desc}")
																except	json.JSONDecodeError:
																				continue
				except	FileNotFoundError:
								print(f"[!]	Could	not	find	{LOG_PATH}.	Has	the	manager	received	any	alert	yet?")
if	__name__	==	"__main__":
				monitor_logs()
EOF
Run	it	(root	access	is	required	because	Wazuh's	log	files	are	protected):
sudo	python3	wazuh_ai_parser.py
Go	do	something	small	on	the	Windows	VM	(lock/unlock	the	screen,	log	off	and	back	on)	and	watch	alerts	print	live	in	this	terminal.	Press	Ctrl+C	to
stop	the	script	at	any	time	—	it	runs	forever	by	design	(it's	watching	a	live	feed),	so	that	is	the	normal	way	to	stop	it,	not	an	error.
14.	Phase	11	—	Add	the	AI	Brain	(OpenAI	Integration)
RUN	THIS	ON:	Ubuntu	VM	(SSH	session)
Never	paste	your	real	API	key	directly	into	a	script.	If	that	file	is	ever	shared,	backed	up,	uploaded	to	GitHub,	or	pasted	into	a	chat,	your	key	leaks	and
someone	else	can	spend	your	money.	Instead,	store	it	as	an	environment	variable	that	the	script	reads	at	run	time.
Set	the	key	as	an	environment	variable	(replace	the	placeholder	with	your	real	key	from	platform.openai.com):
export	OPENAI_API_KEY="sk-REPLACE_WITH_YOUR_OWN_KEY"
This	only	lasts	for	the	current	terminal	session.	To	make	it	permanent,	add	that	same	line	to	the	end	of	
source	~/.bashrc .
~/.bashrc	using	
nano	~/.bashrc ,	then	run
Now	create	the	upgraded	script	that	reads	the	key	from	the	environment	and	sends	high-severity	alerts	to	OpenAI:
cat	<<	'EOF'	>	wazuh_ai_parser.py
import	json
import	os
import	time
import	urllib.request
import	urllib.error
LOG_PATH	=	"/var/ossec/logs/alerts/alerts.json"
AGENT_NAME	=	"Windows-Agent"										#	must	match	your	registered	agent	name
AI_API_URL	=	"https://api.openai.com/v1/chat/completions"
API_KEY	=	os.environ.get("OPENAI_API_KEY")
SEVERITY_THRESHOLD	=	5																#	only	alerts	at/above	this	level	go	to	the	AI
def	analyze_with_ai(level,	description):
				if	not	API_KEY:
								return	"[AI	SKIPPED]	No	OPENAI_API_KEY	set	in	this	terminal	session."
				payload	=	{
								"model":	"gpt-4o-mini",
								"messages":	[
												{"role":	"system",	"content":	"You	are	a	senior	SOC	analyst.	Give	a	concise	2-sentence	threat	assessment	and	one	recommended	
remediation	step	for	this	Windows	security	event."},
												{"role":	"user",	"content":	f"Wazuh	Alert	Level	{level}:	{description}"}
								]
				}
				headers	=	{"Content-Type":	"application/json",	"Authorization":	f"Bearer	{API_KEY}"}
				try:
								req	=	urllib.request.Request(AI_API_URL,	data=json.dumps(payload).encode("utf-8"),
																																						headers=headers,	method="POST")
								with	urllib.request.urlopen(req,	timeout=15)	as	response:
												data	=	json.loads(response.read().decode())
												return	f"\n---	AI	THREAT	TRIAGE	---\n{data['choices'][0]['message']['content']}\n------------------------"
				except	urllib.error.HTTPError	as	e:
								return	f"[AI	API	ERROR]	HTTP	{e.code}:	{e.read().decode()}"
				except	Exception	as	e:
								return	f"[AI	ERROR]	{e}"
def	monitor_logs():
				print(f"[*]	Listening	for	{AGENT_NAME}	events	|	AI	triage	active	for	level	>=	{SEVERITY_THRESHOLD}")
				try:
								with	open(LOG_PATH,	"r")	as	f:
												f.seek(0,	2)
												while	True:
																line	=	f.readline()
																if	not	line:
																				time.sleep(0.5)
																				continue
																try:
																				alert	=	json.loads(line)
																				if	alert.get("agent",	{}).get("name")	==	AGENT_NAME:
																								rule	=	alert.get("rule",	{})
																								level	=	rule.get("level",	0)
																								desc	=	rule.get("description",	"No	description")
																								print(f"\n[RAW	ALERT]	Level:	{level}	|	{desc}")
																								if	level	>=	SEVERITY_THRESHOLD:
																												print(analyze_with_ai(level,	desc))
																								else:
																												print(f"[ROUTINE]	Below	threshold,	no	AI	call	made	(saves	API	cost).")
																except	json.JSONDecodeError:
																				continue
				except	FileNotFoundError:
								print(f"[!]	Could	not	find	{LOG_PATH}")
if	__name__	==	"__main__":
				monitor_logs()
EOF
15.	Phase	12	—	Test	the	Whole	Pipeline	End-to-End
RUN	THIS	ON:	Ubuntu	VM	(SSH	session)
sudo	-E	python3	wazuh_ai_parser.py
Note	the	-E	flag	—	it	tells	
sudo	to	keep	your	environment	variables	(including	
AI	call	silently	gets	skipped	even	after	Phase	11.
OPENAI_API_KEY )	instead	of	wiping	them,	which	is	a	common	reason	the
Everyday	events	like	logging	in	are	usually	level	3	—	you'll	see	them	print	as	routine	with	no	AI	call,	which	is	correct	and	saves	you	money.	To
actually	see	the	AI	respond	during	testing,	you	have	two	honest	options:
Trigger	a	real	level-5+	event,	e.g.	a	failed	login:	on	the	Windows	VM,	lock	the	screen	and	type	the	wrong	password	2–3	times	before	entering	it
correctly.
Or	temporarily	lower	
SEVERITY_THRESHOLD	to	
3	in	the	script	just	for	this	test,	so	ordinary	logins	trigger	the	AI	call	too.	Change	it	back	to	5
afterward	—	leaving	it	at	3	in	real	use	means	every	single	login	burns	API	credit,	which	is	expensive	and	pointless.
A	successful	run	looks	like	this	in	your	terminal:
[RAW	ALERT]	Level:	5	|	Windows	Logon	Failure---	AI	THREAT	TRIAGE	--
Assessment:	A	failed	logon	attempt	was	recorded	on	the	Windows	host,	which	may
indicate	a	mistyped	password	or	a	potential	brute-force	attempt.
Remediation:	Review	the	account's	recent	logon	history	and	enforce	account
lockout	policies	if	repeated	failures	continue.------------------------
If	you	instead	see	
HTTP	429:	credit_balance_exhausted	—	that	is	not	a	bug	in	your	code.	It	means	your	OpenAI	account	has	no	credit	left.	Add	a	small
amount	of	credit	at	platform.openai.com	→	Billing,	and	re-run.	Everything	up	to	that	point	(Wazuh,	the	network,	the	script,	the	API	request	itself)	is	proven	to
be	working	correctly.
16.	Full	Troubleshooting	Ledger	—	Every	Error	We	Hit	&	How	We	Fixed	It
This	is	a	record	of	every	real	problem	encountered	while	building	this	exact	pipeline,	in	the	order	they	tend	to	appear.	If	something	breaks,	find	the
symptom	below	first.
Symptom
Python	script	fails	with
IndentationError
Root	Cause
Fix
Typing	multi-line	Python	by	hand	into	a	terminal
breaks	its	strict	whitespace	rules	—	one	wrong
space	and	it	won't	run.
Never	hand-type	scripts.	Always	create	them	with	the	
cat	<<	'EOF'	>
file.py	block	method	used	throughout	this	guide	—	it	pastes	the	exact
formatting	every	time.
VirtualBox	clipboard	won't	paste
between	host	and	guest
VirtualBox's	shared-clipboard	feature	is	known	to
be	unreliable	on	some	host/guest	combinations,
even	when	set	to	Bidirectional.
Stop	relying	on	it.	Set	up	SSH	from	your	host	into	the	Ubuntu	VM	(Phase	5)	—	a
normal	terminal	window's	copy/paste	always	works.
ssh:	connect	to	host	...
port	22:	Connection	refused
The	SSH	server	(daemon)	isn't	installed	or
running	on	the	Ubuntu	VM	yet.
sudo	apt	install	openssh-server	-y	then	--now	ssh .
sudo	systemctl	enable
Agent	registered	but	dashboard
shows	IP	
.40	while	the	Windows
box	is	actually	
.135	(or	any
similar	mismatch)
The	agent	was	registered	with	a	guessed/example
IP	instead	of	the	machine's	real,	current	IP.
Run	
ipconfig	on	the	Windows	machine	first	(Phase	6).	If	already	registered
wrong,	remove	the	agent	(
manage_agents	→	
R )	and	re-add	it	with	the	correct
IP.
PowerShell	cmdlets	like	
Service	return	"is	not
recognized"
Get
The	terminal	that's	open	is	actually	Command
Prompt	(
cmd.exe ),	not	PowerShell	—	they	look
similar	but	aren't	the	same	shell.
Close	it.	Search	"PowerShell"	in	the	Start	Menu,	right-click	→	Run	as
Administrator,	and	re-run	the	command	there.
Agent	status	stuck	on	"Never
connected"	even	though	the
service	is	running	and	the	config
points	to	the	right	manager	IP
A	firewall	(or	VirtualBox	network	isolation)	is
blocking	TCP	port	1514	between	the	two	VMs.
On	Windows:	
1514 .	If	
Test-NetConnection	-ComputerName	<manager-ip>	-Port
TcpTestSucceeded	:	False ,	open	the	port	on	Ubuntu	with	
ufw	allow	1514/tcp	(Phase	4),	then	
Windows.
Restart-Service	wazuh	on
sudo
Dashboard	homepage	says	"This
instance	has	no	agents	registered"
even	though	agents	exist
A	cosmetic	caching	quirk	in	the	dashboard's
summary	widget	right	after	install/restart	—	it
doesn't	reflect	the	real	agent	index.
Ignore	that	specific	widget.	Go	to	Menu	→	Agents	management	→	Summary	for
the	real,	accurate	list.
Python	script	throws
FileNotFoundError:
/var/ossec/logs/alerts.json
Older	guides	reference	the	file	directly	under
/logs/ .	Current	Wazuh	4.x	versions	nest	it
inside	an	extra	
alerts	folder.
Use	the	correct	path:	
/var/ossec/logs/alerts/alerts.json .
Script	runs	but	never	seems	to	stop Not	actually	a	bug	—	the	script	is	intentionally	an
infinite	loop	tailing	a	live	log	file,	the	same	way
tail	-f	behaves.
Press	Ctrl+C	in	the	terminal	to	stop	it	whenever	you're	done	watching.
Bash	heredoc	script	fails	with	a
syntax	error	around	an	f-string	like
{rule.get('level')}
Assign	the	value	to	a	plain	variable	first	(e.g.	
Mixing	single	quotes	inside	an	f-string	that's	itself
inside	a	bash	heredoc	that	uses	single	quotes
confuses	the	shell's	quote	parsing.
level	=	rule.get("level",
0) )	on	its	own	line,	then	reference	the	variable	in	the	f-string	—	avoid	nested
quotes	inside	
{	}	altogether.
OpenAI	call	returns	
HTTP	429:
credit_balance_exhausted
The	API	key	has	no	billing	credit	left	—	this	is	a
billing	state,	not	a	connectivity	or	code	problem.
Add	credit	at	platform.openai.com	→	Billing.	A	429	response	actually	confirms
your	script	successfully	reached	OpenAI's	servers.
17.	Optimization	&	Security	Hardening	Checklist
The	build	above	works,	but	a	few	things	were	done	the	"quick	and	dirty"	way	to	get	it	running	fast.	Do	these	before	you	call	it	a	portfolio	piece:
1.	Rotate	any	credential	that	ever	touched	a	chat	window.	If	a	password	or	API	key	was	ever	pasted	into	a	chat	(with	an	AI	assistant,	a	friend,
anywhere),	treat	it	as	burned	—	generate	a	new	one.	Chat	logs	are	not	a	safe	place	to	store	secrets,	even	temporarily.
2.	Never	hardcode	API	keys	inside	a	script.	Use	an	environment	variable	(
os.environ.get(...) ,	as	in	Phase	11)	or	a	separate	
.env	file	that	is
excluded	from	version	control.
3.	Change	the	default	Wazuh	dashboard	admin	password	immediately	after	install,	and	don't	reuse	it	anywhere	else.
4.	Use	a	static	IP	or	a	DHCP	reservation	for	the	agent	machine	so	its	address	never	silently	changes	and	breaks	the	registration	(this	directly
prevents	Ledger	row	4).
5.	Keep	an	AI	severity	threshold	in	place	(Phase	11's	
SEVERITY_THRESHOLD )	so	you	only	pay	for	API	calls	on	events	that	matter	—	sending	every
routine	login	to	an	LLM	is	slow	and	needlessly	expensive.
6.	Add	retry/backoff	logic	around	the	OpenAI	call	so	a	temporary	network	hiccup	doesn't	silently	drop	an	important	alert.
7.	Log	the	AI's	responses	to	a	file	(or	a	small	database)	instead	of	only	printing	them	to	the	terminal,	so	you	have	a	permanent,	searchable
record	of	every	triage	the	AI	performed.
8.	Graduate	from	a	custom	polling	script	to	Wazuh's	built-in	Integrations	framework	(
/var/ossec/integrations/ )	for	a	production-grade
version	—	it's	the	officially	supported	way	to	forward	alerts	to	external	services	and	survives	manager	restarts	more	gracefully	than	a	standalone
Python	process.
9.	Set	the	VM	network	mode	correctly	from	day	one	(Phase	2)	rather	than	debugging	it	reactively	—	this	alone	would	have	prevented	roughly
half	the	troubleshooting	in	the	original	build.
18.	What	This	Project	Proves	You	Can	Do
When	you	document	or	talk	about	this	project	(portfolio,	resume,	interview),	these	are	the	concrete,	demonstrable	skills	it	covers:
Standing	up	a	SIEM	(Wazuh)	manager	and	agent	architecture	from	scratch,	across	two	different	operating	systems
Diagnosing	and	fixing	real	network	connectivity	issues	(adapter	modes,	firewall	ports,	TCP	handshake	testing)
Comfortable	use	of	both	Linux	(bash)	and	Windows	(PowerShell)	command-line	environments
Reading	and	parsing	structured	JSON	log	data	programmatically	with	Python
Integrating	a	third-party	REST	API	(OpenAI)	into	a	live	data	pipeline,	including	error	handling	for	HTTP	failures
Basic	security	hygiene:	credential	handling,	environment	variables,	least-privilege	thinking	about	what	should	and	shouldn't	be	hardcoded
Systematic	troubleshooting	—	reproducing	a	symptom,	isolating	the	cause,	verifying	a	fix
19.	Appendix	A	—	Full	Final	Scripts	(Copy-Paste	Ready)
A.1	—	Basic	version	(no	AI,	just	live	log	printing)	—	from	Phase	10
cat	<<	'EOF'	>	wazuh_ai_parser.py
import	json
import	time
LOG_PATH	=	"/var/ossec/logs/alerts/alerts.json"
AGENT_NAME	=	"Windows-Agent"
def	monitor_logs():
				print(f"[*]	Listening	for	live	security	logs	from	{AGENT_NAME}	...")
				try:
								with	open(LOG_PATH,	"r")	as	f:
												f.seek(0,	2)
												while	True:
																line	=	f.readline()
																if	not	line:
																				time.sleep(0.5)
																				continue
																try:
																				alert	=	json.loads(line)
																				if	alert.get("agent",	{}).get("name")	==	AGENT_NAME:
																								rule	=	alert.get("rule",	{})
																								level	=	rule.get("level",	0)
																								desc	=	rule.get("description",	"No	description")
																								print(f"\n[ALERT]	Level:	{level}	|	{desc}")
																except	json.JSONDecodeError:
																				continue
				except	FileNotFoundError:
								print(f"[!]	Could	not	find	{LOG_PATH}.")
if	__name__	==	"__main__":
				monitor_logs()
EOF
A.2	—	Full	version	with	OpenAI	triage	—	from	Phase	11
cat	<<	'EOF'	>	wazuh_ai_parser.py
import	json
import	os
import	time
import	urllib.request
import	urllib.error
LOG_PATH	=	"/var/ossec/logs/alerts/alerts.json"
AGENT_NAME	=	"Windows-Agent"
AI_API_URL	=	"https://api.openai.com/v1/chat/completions"
API_KEY	=	os.environ.get("OPENAI_API_KEY")
SEVERITY_THRESHOLD	=	5
def	analyze_with_ai(level,	description):
				if	not	API_KEY:
								return	"[AI	SKIPPED]	No	OPENAI_API_KEY	set	in	this	terminal	session."
				payload	=	{
								"model":	"gpt-4o-mini",
								"messages":	[
												{"role":	"system",	"content":	"You	are	a	senior	SOC	analyst.	Give	a	concise	2-sentence	threat	assessment	and	one	recommended	
remediation	step	for	this	Windows	security	event."},
												{"role":	"user",	"content":	f"Wazuh	Alert	Level	{level}:	{description}"}
								]
				}
				headers	=	{"Content-Type":	"application/json",	"Authorization":	f"Bearer	{API_KEY}"}
				try:
								req	=	urllib.request.Request(AI_API_URL,	data=json.dumps(payload).encode("utf-8"),
																																						headers=headers,	method="POST")
								with	urllib.request.urlopen(req,	timeout=15)	as	response:
												data	=	json.loads(response.read().decode())
												return	f"\n---	AI	THREAT	TRIAGE	---\n{data['choices'][0]['message']['content']}\n------------------------"
				except	urllib.error.HTTPError	as	e:
								return	f"[AI	API	ERROR]	HTTP	{e.code}:	{e.read().decode()}"
				except	Exception	as	e:
								return	f"[AI	ERROR]	{e}"
def	monitor_logs():
				print(f"[*]	Listening	for	{AGENT_NAME}	events	|	AI	triage	active	for	level	>=	{SEVERITY_THRESHOLD}")
				try:
								with	open(LOG_PATH,	"r")	as	f:
												f.seek(0,	2)
												while	True:
																line	=	f.readline()
																if	not	line:
																				time.sleep(0.5)
																				continue
																try:
																				alert	=	json.loads(line)
																				if	alert.get("agent",	{}).get("name")	==	AGENT_NAME:
																								rule	=	alert.get("rule",	{})
																								level	=	rule.get("level",	0)
																								desc	=	rule.get("description",	"No	description")
																								print(f"\n[RAW	ALERT]	Level:	{level}	|	{desc}")
																								if	level	>=	SEVERITY_THRESHOLD:
																												print(analyze_with_ai(level,	desc))
																								else:
																												print("[ROUTINE]	Below	threshold,	no	AI	call	made	(saves	API	cost).")
																except	json.JSONDecodeError:
																				continue
				except	FileNotFoundError:
								print(f"[!]	Could	not	find	{LOG_PATH}")
if	__name__	==	"__main__":
				monitor_logs()
EOF
20.	Appendix	B	—	One-Page	Command	Cheat	Sheet
Ubuntu	—	Manager	setup
curl	-sO	https://packages.wazuh.com/4.x/wazuh-install.sh
sudo	bash	./wazuh-install.sh	-a
ip	a
sudo	ufw	allow	1514/tcp
sudo	ufw	allow	1515/tcp
sudo	ufw	reload
sudo	apt	install	openssh-server	-y
sudo	systemctl	enable	--now	ssh
Ubuntu	—	Agent	management	&	diagnostics
sudo	/var/ossec/bin/manage_agents								
sudo	/var/ossec/bin/agent_control	-l					
sudo	ss	-tulpn	|	grep	1514															
sudo	systemctl	restart	wazuh-manager
sudo	systemctl	restart	wazuh-dashboard
sudo	systemctl	daemon-reload
#	A	=	add,	E	=	extract	key,	R	=	remove
#	list	connected	agents
#	confirm	manager	is	listening
Windows	—	PowerShell	(Run	as	Administrator)
ipconfig
Get-Service	wazuh
Start-Service	wazuh
Restart-Service	wazuh
Test-NetConnection	-ComputerName	<manager-ip>	-Port	1514
Get-Content	"C:\Program	Files	(x86)\ossec-agent\ossec.conf"	|	Select-String	-Pattern	"address"
Host	machine	—	connecting	in
ssh	yourusername@<ubuntu-ip>
Running	the	pipeline
export	OPENAI_API_KEY="sk-REPLACE_WITH_YOUR_OWN_KEY"
sudo	-E	python3	wazuh_ai_parser.py
#	Ctrl+C	to	stop
You're	done.	If	you	followed	every	phase	in	order,	you	now	have	a	live	SIEM	pipeline	with	AI-assisted	triage,	built	entirely	from	scratch,	and	you	know
exactly	why	each	piece	is	there	and	how	to	fix	it	if	it	breaks
