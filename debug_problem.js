// 先找一个真实会有问题的视频解密
const axios = require('axios');
const cheerio = require('cheerio');

// 解密视频URL函数
function decryptVideoUrl(encryptedUrl) {
    try {
        console.log('输入加密URL:', encryptedUrl);
        for (let offset = 1; offset < 20; offset++) {
            try {
                const testStr = encryptedUrl.substring(offset);
                const decoded = Buffer.from(testStr, 'base64');
                
                console.log(`\n偏移${offset}字节数组前20字节:`, 
                    Array.from(decoded.slice(0, 30)).map(b => ('00'+b.toString(16)).slice(-2)).join(' '));
                
                let startPos = -1;
                // 直接找第一个数字字符，并且后面必须跟着至少5个数字
                for (let i = 0; i < decoded.length - 5; i++) {
                    if (decoded[i] >= 48 && decoded[i] <= 57) {
                        let consecutiveDigits = 0;
                        for (let k = i; k < decoded.length; k++) {
                            if (decoded[k] >= 48 && decoded[k] <= 57) {
                                consecutiveDigits++;
                            } else {
                                break;
                            }
                        }
                        
                        if (consecutiveDigits >= 4) {
                            let slashCount = 0;
                            let hasM3u8 = false;
                            
                            for (let j = i; j < Math.min(i + 100, decoded.length); j++) {
                                if (decoded[j] === 47) {
                                    slashCount++;
                                }
                                
                                if (j >= i + 4) {
                                    if (decoded[j-4] === 46 && 
                                        decoded[j-3] === 109 && 
                                        decoded[j-2] === 51 && 
                                        decoded[j-1] === 117 && 
                                        decoded[j] === 56) {
                                        hasM3u8 = true;
                                        break;
                                    }
                                }
                            }
                            
                            if (slashCount >= 2 && hasM3u8) {
                                startPos = i;
                                console.log(`找到有效起始位置: ${i}, 连续数字: ${consecutiveDigits}`);
                                break;
                            }
                        }
                    }
                }
                
                if (startPos !== -1) {
                    const tempStr = decoded.toString('utf8', startPos);
                    console.log('解密字符串:', tempStr);
                    const m3u8Pos = tempStr.indexOf('.m3u8');
                    if (m3u8Pos !== -1) {
                        const cleanPath = tempStr.substring(0, m3u8Pos + 5);
                        console.log('清理后路径:', cleanPath);
                        return 'https://play.svip30.tv/' + cleanPath;
                    }
                }
            } catch (e) {
                console.error('偏移'+offset+'错误:', e);
            }
        }
        return null;
    } catch (e) {
        console.error('解密错误:', e);
        return null;
    }
}

// 测试你提到的那个 URL 格式
console.log('=== 测试一个真实会返回 vip.123pan.cn 的 ===');

// 让我先试试找这样的加密URL
const fakeTest = '让我先随便找一个';
