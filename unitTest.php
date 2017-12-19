#!/usr/bin/php
<?php

$dir 	= "testFile/";
$exec 	= "expert";
$sufix 	= "Result";

$COLORGREEN = "\033[32m";
$COLORRED 	= "\033[31m";
$COLORCLOSE = "\033[0m";

if (is_dir($dir)) {
	$allerror = "";
	$countAll = 0;
	$countOK = 0;
	if ($dh = opendir($dir)) 
	{
		while (($file = readdir($dh)) !== false)
		{
			if ($file && $file != "." && $file != "..")
			{
				if (!preg_match("/$sufix$/", $file))
				{
					$countAll++;
					$res = shell_exec("./$exec $dir/$file > tmp");
					$res = shell_exec("diff -Bw tmp $dir/$file$sufix");
					unlink("tmp");
					if ($res)
					{
						$allerror .= "$COLORRED [KO] $COLORCLOSE $file:\n";
						$allerror .= "$res";
					}
					else
					{
						$countOK++;
						echo "$COLORGREEN [OK] $COLORCLOSE $file\n";
					}
				}
			}
		}
		closedir($dh);
		echo $allerror;
		if ($countOK == $countAll)
			echo "$COLORGREEN";
		else
			echo "$COLORRED";

		echo " ---------- Total $countOK/$countAll ----------";
		echo "$COLORCLOSE\n";
	}
}
