MacPlayer.Html = '<iframe id="playerCnt" width="100%" frameborder="0" allowfullscreen src="" ></iframe>';
MacPlayer.Show();
var timeout = 0;
var playerInterval = setInterval(function() {
	timeout += 1;
	if(document.getElementById('playerCnt')) {
		document.getElementById('playerCnt').style.height = MacPlayer.Height;
		document.getElementById('playerCnt').src = 'https://yun.92cj.com/acfun58.php?id=' + MacPlayer.Parse + MacPlayer.PlayUrl + '&referer='+ window.location.href;
		clearInterval(playerInterval);
	}
	if (timeout >= 5) {
		clearInterval(playerInterval);
	}
}, 500);