
// 测试新的搜索解析方法
const fs = require('fs');

function fixUrl(url) {
    if (!url) return '';
    if (url.startsWith('//')) {
        return 'https:' + url;
    }
    return url;
}

// 模拟新的搜索解析逻辑
function search(html) {
    const list = [];
    
    if (!html || html.length === 0) {
        return { list: [] };
    }
    
    // 方法1: 使用简单的字符串查找和索引定位
    const dataListStart = html.indexOf('id="data_list"');
    console.log('data_list位置:', dataListStart);
    
    if (dataListStart !== -1) {
        const ulStart = html.lastIndexOf('<ul', dataListStart);
        const ulEnd = html.indexOf('</ul>', dataListStart);
        
        console.log('ulStart:', ulStart, 'ulEnd:', ulEnd);
        
        if (ulStart !== -1 && ulEnd !== -1) {
            const ulContent = html.substring(ulStart, ulEnd + 5);
            console.log('ul内容长度:', ulContent.length);
            
            let pos = 0;
            let count = 0;
            
            while (pos < ulContent.length) {
                const liStart = ulContent.indexOf('<li', pos);
                if (liStart === -1) break;
                
                const liEnd = ulContent.indexOf('</li>', liStart);
                if (liEnd === -1) break;
                
                count++;
                const liContent = ulContent.substring(liStart, liEnd + 5);
                console.log(`\n--- 第${count}个li ---`);
                console.log('li内容:', liContent.substring(0, 200) + '...');
                
                // 提取视频ID
                const hrefStart = liContent.indexOf('href="');
                if (hrefStart !== -1) {
                    const hrefEnd = liContent.indexOf('"', hrefStart + 6);
                    if (hrefEnd !== -1) {
                        const href = liContent.substring(hrefStart + 6, hrefEnd);
                        console.log('href:', href);
                        
                        const vodIdMatch = href.match(/vod-detail-id-(\d+)/);
                        if (vodIdMatch) {
                            const vodId = vodIdMatch[1];
                            console.log('vodId:', vodId);
                            
                            // 提取图片
                            let vodPic = '';
                            const imgStart = liContent.indexOf('<img');
                            if (imgStart !== -1) {
                                const imgEnd = liContent.indexOf('>', imgStart);
                                if (imgEnd !== -1) {
                                    const imgTag = liContent.substring(imgStart, imgEnd + 1);
                                    const dataSrcStart = imgTag.indexOf('data-src="');
                                    if (dataSrcStart !== -1) {
                                        const dataSrcEnd = imgTag.indexOf('"', dataSrcStart + 11);
                                        if (dataSrcEnd !== -1) {
                                            vodPic = imgTag.substring(dataSrcStart + 11, dataSrcEnd);
                                        }
                                    } else {
                                        const srcStart = imgTag.indexOf('src="');
                                        if (srcStart !== -1) {
                                            const srcEnd = imgTag.indexOf('"', srcStart + 5);
                                            if (srcEnd !== -1) {
                                                vodPic = imgTag.substring(srcStart + 5, srcEnd);
                                            }
                                        }
                                    }
                                }
                            }
                            vodPic = fixUrl(vodPic);
                            console.log('vodPic:', vodPic);
                            
                            // 提取标题
                            let vodName = '';
                            const sTitStart = liContent.indexOf('<span class="sTit"');
                            if (sTitStart !== -1) {
                                const spanStart = liContent.indexOf('>', sTitStart);
                                if (spanStart !== -1) {
                                    const spanEnd = liContent.indexOf('</span>', spanStart);
                                    if (spanEnd !== -1) {
                                        vodName = liContent.substring(spanStart + 1, spanEnd).trim();
                                    }
                                }
                            }
                            console.log('vodName:', vodName);
                            
                            list.push({
                                vod_id: vodId,
                                vod_name: vodName,
                                vod_pic: vodPic,
                                vod_remarks: ''
                            });
                        }
                    }
                }
                
                pos = liEnd + 5;
            }
        }
    }
    
    return { list };
}

// 测试
try {
    const html = fs.readFileSync('/workspace/yulinling_search.html', 'utf-8');
    const result = search(html);
    
    console.log('\n=== 最终结果 ===');
    console.log('解析到', result.list.length, '个视频');
    console.log(JSON.stringify(result, null, 2));
} catch (e) {
    console.error('测试出错:', e);
}
