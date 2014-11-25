<?php
	function setFlair($username, $flair){
		$stringToReturn = '<img src="flairs/' . $flair . '.png" height="30px"/> ' . $username;
		return $stringToReturn;
	}
?>

<!DOCTYPE html>
<html lang="en">
<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Plounge Ranks</title>

    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="css/sb-admin-2.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="font-awesome-4.1.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

    <div id="wrapper">

        <!-- Navigation -->
        <nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="index.php">PLounge Rankings</a>
            </div>
            <!-- /.navbar-header -->
            <!-- /.navbar-top-links -->

            <div class="navbar-default sidebar" role="navigation">
                <div class="sidebar-nav navbar-collapse">
                    <ul class="nav" id="side-menu">
                        <li>
                            <a class="active" href="index.php"><i class="fa fa-dashboard fa-fw"></i> Home</a>
                        </li>
						<li>
                            <a href="index.html"> </a>
                        </li>
						<li>
                            <a href="javascript:(function(){var newSS, styles='* { background: white ! important; color: black !important } :link, :link * { color: #55AAFF%20!important%20}%20:visited,%20:visited%20*%20{%20color:%20#AA55FF%20!important%20}';%20if(document.createStyleSheet)%20{%20document.createStyleSheet(%22javascript:'%22+styles+%22'%22);%20}%20else%20{%20newSS=document.createElement('link');%20newSS.rel='stylesheet';%20newSS.href='data:text/css,'+escape(styles);%20document.getElementsByTagName(%22head%22)[0].appendChild(newSS);%20}%20})();"><i class="fa fa-dashboard fa-fw"></i> Light mode</a>
                        </li>
						<li>
                            <a href="javascript:(function(){var newSS, styles='* { background: black ! important; color: white !important } :link, :link * { color: #55AAFF%20!important%20}%20:visited,%20:visited%20*%20{%20color:%20#AA55FF%20!important%20}';%20if(document.createStyleSheet)%20{%20document.createStyleSheet(%22javascript:'%22+styles+%22'%22);%20}%20else%20{%20newSS=document.createElement('link');%20newSS.rel='stylesheet';%20newSS.href='data:text/css,'+escape(styles);%20document.getElementsByTagName(%22head%22)[0].appendChild(newSS);%20}%20})();"><i class="fa fa-dashboard fa-fw"></i> Dark mode</a>
                        </li>
                    </ul>
                </div>
                <!-- /.sidebar-collapse -->
            </div>
            <!-- /.navbar-static-side -->
        </nav>

        <div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">Rankings</h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
			<div class="row">
				<div class="col-lg-12">
                    <div class="panel panel-primary">
                        <div class="panel-heading">
                            About
                        </div>
                        <div class="panel-body">
                            <p>This tool ranks all the PLounge users based on how many comments they have made in the past week. It updates every five minutes.</p>
                        </div>
                        <div class="panel-footer">
                            The list and scripts are by <a href="http://www.reddit.com/user/__Brony__">/u/__Brony__</a>. <br> <font size="1">PHP and hosting by <a href="http://www.reddit.com/u/freepizzafor1dollar">/u/freepizzafor1dollar</a>.</font>
                        </div>
                    </div>
                </div>
			</div>
            <div class="row">
                <div class="col-lg-12">
				
					<div class="panel panel-default">
                        <div class="panel-heading">
                            Last updated <?php echo file_get_contents('lastUpdated.txt'); ?>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <!-- Nav tabs -->
                            <ul class="nav nav-tabs">
                                <li class="active"><a href="#home" data-toggle="tab">Past 24 hours</a>
                                </li>
                                <li><a href="#profile" data-toggle="tab">Past week</a>
                                </li>
                            </ul>

                            <!-- Tab panes -->
                            <div class="tab-content">
                                <div class="tab-pane fade in active" id="home">
									<div class="list-group">
										<?php
											$handle = fopen("statsDay.txt", "r");
											if ($handle) {
												while (($line = fgets($handle)) !== false) {
													$pieces = explode(":", $line);
													$pieces[0] = preg_replace('/\s+/', '', $pieces[0]);
													$pieces[1] = preg_replace('/\s+/', '', $pieces[1]);
													$pieces[2] = preg_replace('/\s+/', '', $pieces[2]);
													
													//Site Mod Badge
													//if(strcmp($pieces[1], "Freepizzafor1dollar") == 0 || strcmp($pieces[1], "__brony__") == 0){
														//$pieces[1] = setFlair($pieces[1], "ppapprove");
													//}
													//Mod Badge
													//if(strcmp($pieces[1], "LunarWolves") == 0 || strcmp($pieces[1], "DaylightDarkle") == 0 || strcmp($pieces[1], "french_guy_al") == 0 || strcmp($pieces[1], "DoomedCivilian") == 0){
														//$pieces[1] = setFlair($pieces[1], "cutiemarkcrusaders");
													//}
													//Pinkie_Pie Badges
													//if(strcmp($pieces[1], "Pinkie_Pie") == 0){
														//$pieces[1] = '<img src="bot.png" height="30px"/><img src="cutiemarkcrusaders.png" height="30px"/> Pinkie_Pie';
													//}
													//Bot Badges
													//if(strcmp($pieces[1], "xkcd_transcriber") == 0 || strcmp($pieces[1], "autowikibot") == 0){
														//$pieces[1] = setFlair($pieces[1], "bot");
													//}
													//if(strcmp($pieces[1], "Freepizzafor1dollar") == 0){
														//$pieces[1] = "[BANNED]";
														//$pieces[2] = "0";
													//}
													
													print '<a href="user.php?user=' . $pieces[1] . '" class="list-group-item">';
													print '<i class="fa fa-comment fa-fw"></i>  ' . $pieces[0] . ' ' . $pieces[1];
													print '<span class="pull-right text-muted small"><em>' . $pieces[2] . '</em></span></a>';
												}
											} else {
												// error opening the file.
											} 
											fclose($handle);
										?>
									</div>
									<!-- /.list-group -->
                                </div>
                                <div class="tab-pane fade" id="profile">
                                    <div class="list-group">
										<?php
											$handle = fopen("statsWeek.txt", "r");
											if ($handle) {
												while (($line = fgets($handle)) !== false) {
													$pieces = explode(":", $line);
													$pieces[0] = preg_replace('/\s+/', '', $pieces[0]);
													$pieces[1] = preg_replace('/\s+/', '', $pieces[1]);
													$pieces[2] = preg_replace('/\s+/', '', $pieces[2]);
													
													//Site Mod Badge
													//if(strcmp($pieces[1], "Freepizzafor1dollar") == 0 || strcmp($pieces[1], "__brony__") == 0){
														//$pieces[1] = setFlair($pieces[1], "ppapprove");
													//}
													//Mod Badge
													//if(strcmp($pieces[1], "LunarWolves") == 0 || strcmp($pieces[1], "DaylightDarkle") == 0 || strcmp($pieces[1], "french_guy_al") == 0 || strcmp($pieces[1], "DoomedCivilian") == 0){
														//$pieces[1] = setFlair($pieces[1], "cutiemarkcrusaders");
													//}
													//Pinkie_Pie Badges
													//if(strcmp($pieces[1], "Pinkie_Pie") == 0){
														//$pieces[1] = '<img src="bot.png" height="30px"/><img src="cutiemarkcrusaders.png" height="30px"/> Pinkie_Pie';
													//}
													//Bot Badges
													//if(strcmp($pieces[1], "xkcd_transcriber") == 0 || strcmp($pieces[1], "autowikibot") == 0){
														//$pieces[1] = setFlair($pieces[1], "bot");
													//}
													
													//if(strcmp($pieces[1], "ParaspriteHugger") == 0){
														//$pieces[1] = "[BANNED]";
													//}
													
													print '<a href="user.php?user=' . $pieces[1] . '" class="list-group-item">';
													print '<i class="fa fa-comment fa-fw"></i>  ' . $pieces[0] . ' ' . $pieces[1];
													print '<span class="pull-right text-muted small"><em>' . $pieces[2] . '</em></span></a>';
												}
											} else {
												// error opening the file.
											} 
											fclose($handle);
										?>
									</div>
									<!-- /.list-group -->
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
				
                    
                </div>
            </div>
            <!-- /.row -->
        </div>
        <!-- /#page-wrapper -->

    </div>
    <!-- /#wrapper -->

	<!-- jQuery -->
    <script src="js/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>
	

</body>

</html>
