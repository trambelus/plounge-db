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
	
	<!-- Morris Charts CSS -->
    <link href="css/plugins/morris.css" rel="stylesheet">

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
                    <h1 class="page-header"><?php echo $_GET['user']; ?> - Statistics</h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
            <div class="row">
                <div class="col-lg-12">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-bar-chart-o fa-fw"></i> Daily activity by hour
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <div id="morris-area-chart"></div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
            </div>
			<div class="row">
				<div class="col-lg-12">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-bar-chart-o fa-fw"></i> Activity for the past month
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <div id="morris-area-chart-2"></div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
			</div>
            <!-- /.row -->
			<div class="row">
				<div class="col-lg-6">
					<div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-bell fa-fw"></i> People who replied to user
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <div class="list-group" id="UsersWhoReplied">
                                
                            </div>
                            <!-- /.list-group -->
                        </div>
                        <!-- /.panel-body -->
					</div>
				</div>
				<div class="col-lg-6">
					<div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-bell fa-fw"></i> People user replied to
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <div class="list-group" id="UsersRepliedTo">
                                
                            </div>
                            <!-- /.list-group -->
                        </div>
                        <!-- /.panel-body -->
					</div>
				</div>
			</div>
        </div>
        <!-- /#page-wrapper -->

    </div>
    <!-- /#wrapper -->

	<!-- jQuery -->
    <script src="js/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>
	
	<!-- Morris Charts JavaScript -->
    <script src="js/plugins/morris/raphael.min.js"></script>
    <script src="js/plugins/morris/morris.min.js"></script>
	
	<script src="userstats/<?php echo $_GET['user']; ?>.js"></script>
	
</body>

</html>
