<#
Watchdog Powershellmodule

update: 
wget https://raw.githubusercontent.com/blacktorch96/PySchTasksGenerator/main/watchdog.ps1 -outfile watchdog.ps1

#>
function watchdog($servername, $dienstname, $status, $comment, $debug=$false) {
	if ($servername -eq "") {$servername=$env:computername}
    $hostx = "http://grp-statistik.stellenanzeigen.de"
    $uri = ($hostx + "/status/update.asp?" + "s=" + $status + "&sn=" + $servername + "&d=" + $dienstname + "&c=" + $comment)
    $ret = (invoke-webrequest $uri -UseBasicParsing).Content
    if ($debug) {
        Write-Host $ret
    }
}

function watchdog-start($dienstname, $servername="", $comment="") {
	watchdog -servername $servername -dienstname $dienstname -status "1" -comment $comment
}

function watchdog-end($dienstname, $servername="", $comment="") {
	watchdog -servername $servername -dienstname $dienstname -status "0" -comment $comment
}

function watchdog-update($dienstname, $servername="", $comment="") {
	watchdog -servername $servername -dienstname $dienstname -status "1" -comment $comment
}

function watchdog-error($dienstname, $servername="", $comment="") {
	watchdog -servername $servername -dienstname $dienstname -status "2" -comment $comment
}
