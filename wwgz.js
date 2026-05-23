
const ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Mobile/15E148 Safari/604.1'
const HOST = 'https://vip.wwgz.cn:5200'
const PLAY_HOST = 'https://api.nmvod.me:520'

async function request(reqUrl, postData = null) {
    let headers = {
        'User-Agent': ua,
        'Referer': HOST + '/'
    }
    let res = await req(reqUrl, {
        method: postData ? 'post' : 'get',
        headers: headers,
        data: postData,
        dataType: 'text',
        timeout: 20000
    })
    return res.content
}

var rule = {
    title: '农民影视',
    host: HOST,
    url: '',
    searchUrl: '/index.php?m=vod-search',
    searchable: 1,
    quickSearch: 0,
    filterable: 1,
    filterObj: {
        1: [
            {
                key: 'type',
                name: '类型',
                value: [
                    { n: '全部', v: '1' },
                    { n: '动作片', v: '5' },
                    { n: '喜剧片', v: '6' },
                    { n: '爱情片', v: '7' },
                    { n: '科幻片', v: '8' },
                    { n: '恐怖片', v: '9' },
                    { n: '剧情片', v: '10' },
                    { n: '战争片', v: '11' },
                    { n: '惊悚片', v: '12' },
                    { n: '奇幻片', v: '13' },
                ],
            },
            {
                key: 'area',
                name: '地区',
                value: [
                    { n: '全部', v: '' },
                    { n: '大陆', v: '大陆' },
                    { n: '香港', v: '香港' },
                    { n: '台湾', v: '台湾' },
                    { n: '美国', v: '美国' },
                    { n: '日本', v: '日本' },
                    { n: '韩国', v: '韩国' },
                    { n: '印度', v: '印度' },
                    { n: '泰国', v: '泰国' },
                    { n: '英国', v: '英国' },
                    { n: '法国', v: '法国' },
                    { n: '加拿大', v: '加拿大' },
                    { n: '西班牙', v: '西班牙' },
                    { n: '俄罗斯', v: '俄罗斯' },
                    { n: '其他', v: '其他' },
                ],
            },
            {
                key: 'year',
                name: '年份',
                value: [
                    { n: '全部', v: '' },
                    { n: '2026', v: '2026' },
                    { n: '2025', v: '2025' },
                    { n: '2024', v: '2024' },
                    { n: '2023', v: '2023' },
                    { n: '2022', v: '2022' },
                    { n: '2021', v: '2021' },
                    { n: '2020', v: '2020' },
                    { n: '2019', v: '2019' },
                    { n: '2018', v: '2018' },
                    { n: '2017', v: '2017' },
                    { n: '2016', v: '2016' },
                    { n: '2015', v: '2015' },
                    { n: '2014', v: '2014' },
                    { n: '2013', v: '2013' },
                    { n: '2012', v: '2012' },
                    { n: '2011', v: '2011' },
                    { n: '2010', v: '2010' },
                    { n: '2009~2000', v: '2009~2000' },
                ],
            },
            {
                key: 'sort',
                name: '排序',
                value: [
                    { n: '时间', v: 'time' },
                    { n: '人气', v: 'hits' },
                    { n: '评分', v: 'score' },
                ],
            },
        ],
        2: [
            {
                key: 'type',
                name: '类型',
                value: [
                    { n: '全部', v: '2' },
                    { n: '国产剧', v: '12' },
                    { n: '港台泰', v: '13' },
                    { n: '日韩剧', v: '14' },
                    { n: '欧美剧', v: '15' },
                ],
            },
            {
                key: 'area',
                name: '地区',
                value: [
                    { n: '全部', v: '' },
                    { n: '大陆', v: '大陆' },
                    { n: '香港', v: '香港' },
                    { n: '台湾', v: '台湾' },
                    { n: '美国', v: '美国' },
                    { n: '日本', v: '日本' },
                    { n: '韩国', v: '韩国' },
                    { n: '印度', v: '印度' },
                    { n: '泰国', v: '泰国' },
                    { n: '英国', v: '英国' },
                    { n: '法国', v: '法国' },
                    { n: '加拿大', v: '加拿大' },
                    { n: '西班牙', v: '西班牙' },
                    { n: '俄罗斯', v: '俄罗斯' },
                    { n: '其他', v: '其他' },
                ],
            },
            {
                key: 'year',
                name: '年份',
                value: [
                    { n: '全部', v: '' },
                    { n: '2026', v: '2026' },
                    { n: '2025', v: '2025' },
                    { n: '2024', v: '2024' },
                    { n: '2023', v: '2023' },
                    { n: '2022', v: '2022' },
                    { n: '2021', v: '2021' },
                    { n: '2020', v: '2020' },
                    { n: '2019', v: '2019' },
                    { n: '2018', v: '2018' },
                    { n: '2017', v: '2017' },
                    { n: '2016', v: '2016' },
                    { n: '2015', v: '2015' },
                    { n: '2014', v: '2014' },
                    { n: '2013', v: '2013' },
                    { n: '2012', v: '2012' },
                    { n: '2011', v: '2011' },
                    { n: '2010', v: '2010' },
                ],
            },
            {
                key: 'sort',
                name: '排序',
                value: [
                    { n: '时间', v: 'time' },
                    { n: '人气', v: 'hits' },
                    { n: '评分', v: 'score' },
                ],
            },
        ],
        3: [
            {
                key: 'area',
                name: '地区',
                value: [
                    { n: '全部', v: '' },
                    { n: '大陆', v: '大陆' },
                    { n: '香港', v: '香港' },
                    { n: '台湾', v: '台湾' },
                    { n: '美国', v: '美国' },
                    { n: '日本', v: '日本' },
                    { n: '韩国', v: '韩国' },
                    { n: '印度', v: '印度' },
                    { n: '泰国', v: '泰国' },
                    { n: '英国', v: '英国' },
                    { n: '法国', v: '法国' },
                    { n: '加拿大', v: '加拿大' },
                    { n: '西班牙', v: '西班牙' },
                    { n: '俄罗斯', v: '俄罗斯' },
                    { n: '其他', v: '其他' },
                ],
            },
            {
                key: 'year',
                name: '年份',
                value: [
                    { n: '全部', v: '' },
                    { n: '2026', v: '2026' },
                    { n: '2025', v: '2025' },
                    { n: '2024', v: '2024' },
                    { n: '2023', v: '2023' },
                    { n: '2022', v: '2022' },
                    { n: '2021', v: '2021' },
                    { n: '2020', v: '2020' },
                    { n: '2019', v: '2019' },
                    { n: '2018', v: '2018' },
                    { n: '2017', v: '2017' },
                    { n: '2016', v: '2016' },
                    { n: '2015', v: '2015' },
                    { n: '2014', v: '2014' },
                    { n: '2013', v: '2013' },
                    { n: '2012', v: '2012' },
                    { n: '2011', v: '2011' },
                    { n: '2010', v: '2010' },
                ],
            },
            {
                key: 'sort',
                name: '排序',
                value: [
                    { n: '时间', v: 'time' },
                    { n: '人气', v: 'hits' },
                    { n: '评分', v: 'score' },
                ],
            },
        ],
        4: [
            {
                key: 'area',
                name: '地区',
                value: [
                    { n: '全部', v: '' },
                    { n: '大陆', v: '大陆' },
                    { n: '香港', v: '香港' },
                    { n: '台湾', v: '台湾' },
                    { n: '美国', v: '美国' },
                    { n: '日本', v: '日本' },
                    { n: '韩国', v: '韩国' },
                    { n: '印度', v: '印度' },
                    { n: '泰国', v: '泰国' },
                    { n: '英国', v: '英国' },
                    { n: '法国', v: '法国' },
                    { n: '加拿大', v: '加拿大' },
                    { n: '西班牙', v: '西班牙' },
                    { n: '俄罗斯', v: '俄罗斯' },
                    { n: '其他', v: '其他' },
                ],
            },
            {
                key: 'year',
                name: '年份',
                value: [
                    { n: '全部', v: '' },
                    { n: '2026', v: '2026' },
                    { n: '2025', v: '2025' },
                    { n: '2024', v: '2024' },
                    { n: '2023', v: '2023' },
                    { n: '2022', v: '2022' },
                    { n: '2021', v: '2021' },
                    { n: '2020', v: '2020' },
                    { n: '2019', v: '2019' },
                    { n: '2018', v: '2018' },
                    { n: '2017', v: '2017' },
                    { n: '2016', v: '2016' },
                    { n: '2015', v: '2015' },
                    { n: '2014', v: '2014' },
                    { n: '2013', v: '2013' },
                    { n: '2012', v: '2012' },
                    { n: '2011', v: '2011' },
                    { n: '2010', v: '2010' },
                ],
            },
            {
                key: 'sort',
                name: '排序',
                value: [
                    { n: '时间', v: 'time' },
                    { n: '人气', v: 'hits' },
                    { n: '评分', v: 'score' },
                ],
            },
        ],
        26: [],
    },
    class_name: '电影&amp;连续剧&amp;综艺&amp;动漫&amp;短剧',
    class_url: '1&amp;2&amp;3&amp;4&amp;26',
    lazy: 'js',
    timeout: 20000,
    play_parse: true
}

async function init(cfg) {
    await js2proxy(rule)
}

async function home(filter) {
    let html = await request(HOST)
    let $ = load(html)
    let classes = []
    let tabs = [
        { name: '电影', id: '1' },
        { name: '连续剧', id: '2' },
        { name: '综艺', id: '3' },
        { name: '动漫', id: '4' },
        { name: '短剧', id: '26' },
    ]
    for (let i = 0; i &lt; tabs.length; i++) {
        let tab = tabs[i]
        classes.push({
            type_id: tab.id,
            type_name: tab.name
        })
    }
    let vods = []
    $('section.mod li').each((_, element) =&gt; {
        const $element = $(element)
        const a = $element.find('a').first()
        const href = a.attr('href')
        const title = a.attr('title')
        const img = $element.find('img').first()
        const cover = img.attr('src') || img.attr('data-src')
        const subTitle = $element.find('.sDes').text()
        if (title) {
            vods.push({
                vod_id: href,
                vod_name: title,
                vod_pic: cover,
                vod_remarks: subTitle || '',
            })
        }
    })
    return JSON.stringify({
        class: classes,
        list: vods
    })
}

async function homeVod() {
    let html = await request(HOST)
    let $ = load(html)
    let videos = []
    $('section.mod li').each((_, element) =&gt; {
        const $element = $(element)
        const a = $element.find('a').first()
        const href = a.attr('href')
        const title = a.attr('title')
        const img = $element.find('img').first()
        const cover = img.attr('src') || img.attr('data-src')
        const subTitle = $element.find('.sDes').text()
        if (title) {
            videos.push({
                vod_id: href,
                vod_name: title,
                vod_pic: cover,
                vod_remarks: subTitle || '',
            })
        }
    })
    return JSON.stringify({ list: videos })
}

async function category(tid, pg, filter, extend) {
    const page = pg || 1
    const url = `${HOST}/vod-list-id-${extend?.type || tid}-pg-${page}-order--by-${extend?.sort || 'time'}-class-0-year-${extend?.year || 0}-letter--area-${extend?.area || ''}-lang-.html`
    const html = await request(url)
    const $ = load(html)
    const videos = []
    $('.globalPicList &gt; ul li').each((_, element) =&gt; {
        const $element = $(element)
        const href = $element.find('a').attr('href')
        const title = $element.find('a').attr('title')
        const cover = $element.find('img').attr('src')
        const subTitle = $element.find('.sDes').text()
        if (title) {
            videos.push({
                vod_id: href,
                vod_name: title,
                vod_pic: cover,
                vod_remarks: subTitle || '',
            })
        }
    })
    const filterData = rule.filterObj[tid] || []
    return JSON.stringify({
        list: videos,
        page: parseInt(page),
        pagecount: 999,
        limit: 24,
        total: 9999,
        filters: { '1': filterData }
    })
}

async function detail(id) {
    let html = await request(HOST + id)
    const $ = load(html)
    let vod = {}
    vod.vod_name = $('.globalVideoInfo h1').text()
    vod.vod_actor = $('.globalVideoInfo .part:contains("主演")').text().replace(/主演[：:]/, '')
    vod.vod_director = $('.globalVideoInfo .part:contains("导演")').text().replace(/导演[：:]/, '')
    vod.vod_content = $('.globalVideoInfo .part:contains("简介")').text().replace(/简介[：:]/, '')
    vod.vod_remarks = $('.globalVideoInfo .part:contains("状态")').text().replace(/状态[：:]/, '')
    vod.vod_pic = $('.globalVideoInfo .pic img').attr('src')
    
    let lists = []
    let firstEpUrl = null
    $('.numList').each((i, numList) =&gt; {
        let playlist = {
            name: $(numList).prev('.title').text() || '播放列表',
            list: []
        }
        $(numList).find('li a').each((_, a) =&gt; {
            let name = $(a).text()
            let url = $(a).attr('href')
            if (i === 0 &amp;&amp; !firstEpUrl) firstEpUrl = url
            playlist.list.push(name + '$' + url)
        })
        if (playlist.list.length &gt; 0) lists.push(playlist)
    })
    
    let vod_play_from = []
    let vod_play_url = []
    for (let i = 0; i &lt; lists.length; i++) {
        vod_play_from.push(lists[i].name)
        vod_play_url.push(lists[i].list.join('#'))
    }
    
    vod.vod_play_from = vod_play_from.join('$$$')
    vod.vod_play_url = vod_play_url.join('$$$')
    
    return JSON.stringify({ list: [vod] })
}

async function play(flag, id, flags) {
    const playUrl = `${PLAY_HOST}/player/?url=${id}`
    const html = await request(playUrl)
    
    const match = html.match(/var\s+config\s*=\s*(\{[\s\S]*?\})/)
    if (!match) {
        return JSON.parse({ parse: 0 })
    }
    
    const configString = match[1]
    const playUrlMatch = configString.match(/url":\s*"(.+?)"/)
    if (!playUrlMatch) {
        return JSON.parse({ parse: 0 })
    }
    
    let url = playUrlMatch[1]
    
    try {
        if (url.includes('%')) {
            url = decodeURIComponent(url)
        }
    } catch (e) {
    }
    
    try {
        let decoded = decryptVideoUrl(url)
        if (decoded) {
            url = decoded
        }
    } catch (e) {
    }
    
    return JSON.stringify({
        parse: 1,
        url: url,
        header: {
            'User-Agent': ua,
            'Referer': HOST + '/'
        }
    })
}

function decryptVideoUrl(encryptedUrl) {
    try {
        let bytes = []
        if (typeof encryptedUrl === 'string') {
            for (let i = 0; i &lt; encryptedUrl.length; i++) {
                bytes.push(encryptedUrl.charCodeAt(i))
            }
        } else {
            bytes = encryptedUrl
        }
        
        let m3u8Pattern = [46, 109, 51, 117, 56]
        let m3u8Index = -1
        for (let i = 0; i &lt;= bytes.length - 5; i++) {
            if (bytes[i] === m3u8Pattern[0] &amp;&amp;
                bytes[i + 1] === m3u8Pattern[1] &amp;&amp;
                bytes[i + 2] === m3u8Pattern[2] &amp;&amp;
                bytes[i + 3] === m3u8Pattern[3] &amp;&amp;
                bytes[i + 4] === m3u8Pattern[4]) {
                m3u8Index = i
                break
            }
        }
        
        if (m3u8Index === -1) {
            return null
        }
        
        let startIndex = -1
        for (let i = m3u8Index; i &gt;= 0; i--) {
            let byte = bytes[i]
            if ((byte &gt;= 97 &amp;&amp; byte &lt;= 122) || (byte &gt;= 65 &amp;&amp; byte &lt;= 90)) {
            } else if (byte &gt;= 48 &amp;&amp; byte &lt;= 57) {
            } else if (byte === 46 || byte === 58 || byte === 47 || byte === 45 || byte === 95) {
            } else {
                startIndex = i + 1
                break
            }
        }
        if (startIndex === -1) startIndex = 0
        
        let result = ''
        for (let i = startIndex; i &lt;= m3u8Index + 4; i++) {
            result += String.fromCharCode(bytes[i])
        }
        
        if (!result.startsWith('http')) {
            return null
        }
        
        return result
    } catch (e) {
        return null
    }
}

async function search(wd, quick) {
    const text = encodeURIComponent(wd)
    const page = quick || 1
    const url = `${HOST}/index.php?m=vod-search`
    if (page &gt; 1) return JSON.stringify({ list: [] })
    const body = `wd=${text}`
    const html = await request(url, body)
    const $ = load(html)
    const videos = []
    $('#search_main ul li').each((_, element) =&gt; {
        const $element = $(element)
        const href = $element.find('.pic a').attr('href')
        const title = $element.find('.sTit').text()
        const cover = $element.find('img').attr('data-src')
        const subTitle = $element.find('.sStyle').text()
        if (title) {
            videos.push({
                vod_id: href,
                vod_name: title,
                vod_pic: cover,
                vod_remarks: subTitle || '',
            })
        }
    })
    return JSON.stringify({ list: videos })
}
