<html>
<head>
<title><?php echo getcwd(); ?></title>
<style type='text/css'>
body {
    font-family: "Corbel", sans-serif;
    font-size: 9pt;
    line-height: 10.5pt;
}

ul.subdirs {
    padding: 0pt;
}
li.subdirs {
    display: inline;
    list-style-type: none;
    padding-right: 20px;
}

div.pic h3 { 
    font-size: 11pt;
    margin: 0.5em 1em 0.2em 1em;
}
div.pic p {
    font-size: 11pt;
    margin: 0.2em 1em 0.1em 1em;
}
div.pic {
    display: block;
    float: left;
    background-color: white;
    border: 1px solid #ccc;
    padding: 2px;
    text-align: center;
    margin: 2px 10px 10px 2px;

//     -moz-box-shadow: 7px 5px 5px rgb(80,80,80);    /* Firefox 3.5 */
//     -webkit-box-shadow: 7px 5px 5px rgb(80,80,80); /* Chrome, Safari */
//     box-shadow: 7px 5px 5px rgb(80,80,80);         /* New browsers */  
}
a { text-decoration: none; color: rgb(0,0,80); }
a:hover { text-decoration: underline; color: rgb(255,80,80); }
</style>
</head>
<body>
<br>
<h1><?php echo getcwd(); ?></h1>
<h2>
<?php
print "<ul class='subdirs'>";
print "<li class='subdirs'>Subdirs</li>";
if (file_exists("../index.php")) {
    print "<li class='subdirs'><a href=\"../\">[..]</a></li>";
}
$subdirs = glob('*', GLOB_ONLYDIR);
if (count($subdirs) != 0 ) { 
    foreach($subdirs as $dir) {
        print "<li class='subdirs'><a href=".$dir.">[".$dir."]</a></li>";
    }
}
print "</ul>";
?>
</h2>
<h2><a name="plots">Plots</a></h2>
<p><form>Filter: <input type="text" name="match" size="30" value="<?php if (isset($_GET['match'])) print htmlspecialchars($_GET['match']);  ?>" /><input type="Submit" value="Go" /></form></p>

<div>
<?php
$plotwidth = '400px';
$displayed = array();
array_push($displayed,basename($_SERVER['PHP_SELF']));
if ($_GET['noplots']) {
    print "Plots will not be displayed.\n";
} else {
    $other_exts = array('.pdf', '.cxx', '.eps', '.root', '.txt');
    $filenames = glob("*.png"); sort($filenames);
    foreach ($filenames as $filename) {
        if (isset($_GET['match']) && !fnmatch('*'.$_GET['match'].'*', $filename)) continue;
        array_push($displayed, $filename);
        print "<div class='pic'>\n";
        print "<h3><a href=\"$filename\">$filename</a></h3>";
        print "<a href=\"$filename\"><img src=\"$filename\" style=\"border: none; width: $plotwidth; \"></a>";
        $others = array();
        foreach ($other_exts as $ex) {
            $other_filename = str_replace('.png', $ex, $filename);
            if (file_exists($other_filename)) {
                array_push($others, "<a class=\"file\" href=\"$other_filename\">[" . $ex . "]</a>");
                if ($ex != '.txt') array_push($displayed, $other_filename);
            }
        }
        if ($others) print "<p>Also as ".implode(', ',$others)."</p>";
        print "</div>";
    }
}
?>
</div>
<div style="display: block; clear:both;">
<h2><a name="files">Other files</a></h2>
<ul>
<?
foreach (glob("*") as $filename) {
    if ($_GET['noplots'] || !in_array($filename, $displayed)) {
        if (isset($_GET['match']) && !fnmatch('*'.$_GET['match'].'*', $filename)) continue;
        if (is_dir($filename)) {
            print "<li>[DIR] <a href=\"$filename\">$filename</a></li>";
        } else {
            print "<li><a href=\"$filename\">$filename</a></li>";
        }
    }
}
?>
</ul>
</div>
</body>
</html>
