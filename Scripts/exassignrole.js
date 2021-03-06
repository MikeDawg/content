//+ exchange/assign.ps1

//Params:
//See here: https://technet.microsoft.com/en-us/library/dd298173(v=exchg.160).aspx
//query is the string provided to the -SearchQuery parameter
//to-mailbox is the string provided to -TargetMailbox parameter
//to-folder is the string provided to -TargetFolder parameter
//if server is provided, it'll be used as -ServerFQDN parameter to Connect-ExchangeServer cmdlet

if ((env.ARCH !== "amd64") && (env.OS !== "windows")) {
    throw("Script can run only in 64bit Windows Agents");
}

var command = [];
command.push("powershell.exe");
command.push("-version 2.0");
command.push("-NonInteractive");
command.push("-NoLogo");
command.push(which("assign.ps1"));
if (typeof (args.role) !== "undefined") {
    command.push("-role");
    command.push(args.role);
}
if (typeof (args.username) !== "undefined") {
    command.push("-username");
    command.push(args.username);
}
if (typeof (args.server) !== "undefined") {
    command.push("-server");
    command.push(args.server);
}

pack(execute(command.join(" ")), 'table');
