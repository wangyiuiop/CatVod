const https = require('https');
const http = require('http');

const USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1';

const BASE_URL = 'vip.wwgz.cn:5200';

const CATEGORIES = {
  '1': '电影',
  '2': '连续剧',
  '3': '综艺',
  '4': '动漫',
  '26': '短剧',
  '20': '小姐姐',
  '31': '音乐'
};

function fetchPage(url, callback) {
  const options = {
    hostname: BASE_URL.split(':')[0],
    port: 443,
    path: url,
    method: 'GET',
    headers: {
      'User-Agent': USER_AGENT,
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Connection': 'keep-alive'
    }
  };

  const req = https.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => {
      data += chunk;
    });
    res.on('end', () => {
      callback(null, data);
    });
  });

  req.on('error', (error) => {
    callback(error, null);
  });

  req.end();
}

function parseList(html) {
  const items = [];
  const regex = /<li><a href="\/vod-detail-id-(\d+)\.html" title="([^"]+)">[\s\S]*?data-echo="([^"]+)"[\s\S]*?<span class="sTit">([^<]+)<\/span>[\s\S]*?<span class="sDes">([^<]+)<\/span>/g;
  
  let match;
  while ((match = regex.exec(html)) !== null) {
    items.push({
      id: match[1],
      title: match[2],
      pic: match[3],
      name: match[4],
      des: match[5]
    });
  }
  
  return items;
}

function parseDetail(html) {
  const result = {};
  
  const titleMatch = html.match(/<h1 class="title"><a href="[^"]*" title="([^"]+)">/);
  if (titleMatch) result.title = titleMatch[1];
  
  const picMatch = html.match(/<section class="page-hd"><a href="[^"]*" title="[^"]*"><img src="([^"]+)"/);
  if (picMatch) result.pic = picMatch[1];
  
  const actorMatch = html.match(/主演:&nbsp;<\/span>([^<]+)/);
  if (actorMatch) result.actor = actorMatch[1].trim();
  
  const directorMatch = html.match(/导演:&nbsp;<\/span>([^<]+)/);
  if (directorMatch) result.director = directorMatch[1].trim();
  
  const yearMatch = html.match(/年代:&nbsp;<\/span><a[^>]*>([^<]+)<\/a>/);
  if (yearMatch) result.year = yearMatch[1];
  
  const descMatch = html.match(/简[\s&nbsp;]+介：([^<]+)<\/p>/);
  if (descMatch) result.content = descMatch[1].trim();
  
  const playList = [];
  const playRegex = /<a href="\/vod-play-id-\d+-src-\d+-num-\d+\.html"[^>]*>([^<]+)<\/a>/g;
  let playMatch;
  while ((playMatch = playRegex.exec(html)) !== null) {
    playList.push(playMatch[1].trim());
  }
  result.playList = playList;
  
  return result;
}

function getCategories() {
  return Object.entries(CATEGORIES).map(([id, name]) => ({
    type_id: id,
    type_name: name
  }));
}

function getCategoryUrl(typeId, page = 1, order = 'time') {
  const orderMap = {
    'time': 'time',
    'hits': 'hits',
    'score': 'score'
  };
  const orderBy = orderMap[order] || 'time';
  return `/index.php?m=vod-list-id-${typeId}-pg-${page}-order--by-${orderBy}-class-0-year-0-letter--area--lang-.html`;
}

function getDetailUrl(id) {
  return `/vod-detail-id-${id}.html`;
}

function getPlayUrl(id, src = 1, num = 1) {
  return `/vod-play-id-${id}-src-${src}-num-${num}.html`;
}

function getSearchUrl(keyword) {
  return `/index.php?m=vod-search&wd=${encodeURIComponent(keyword)}`;
}

module.exports = {
  fetchPage,
  parseList,
  parseDetail,
  getCategories,
  getCategoryUrl,
  getDetailUrl,
  getPlayUrl,
  getSearchUrl,
  BASE_URL,
  USER_AGENT
};
