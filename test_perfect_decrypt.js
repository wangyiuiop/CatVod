// 完美解密函数
function decryptVideoUrl(encryptedUrl) {
    try {
        for (let offset = 1; offset < 20; offset++) {
            try {
                const testStr = encryptedUrl.substring(offset);
                const decoded = Buffer.from(testStr, 'base64');
                
                // 找 .m3u8 的具体字节位置
                // .m3u8 对应的字节是：46, 109, 51, 117, 56
                let m3u8Pos = -1;
                for (let i = 0; i < decoded.length - 4; i++) {
                    if (decoded[i] === 46 &&
                        decoded[i+1] === 109 &&
                        decoded[i+2] === 51 &&
                        decoded[i+3] === 117 &&
                        decoded[i+4] === 56) {
                        m3u8Pos = i;
                        break;
                    }
                }
                
                if (m3u8Pos !== -1) {
                    // 找到了 .m3u8！现在往回找路径的起始点
                    // 要找到连续有效字符的起点，找到连续的非乱码字符
                    let startPos = 0;
                    let consecutiveValid = 0;
                    
                    // 从 m3u8Pos 往回找
                    for (let i = m3u8Pos; i >= 0; i--) {
                        const byte = decoded[i];
                        // 有效的ASCII字符
                        if ((byte >= 32 && byte <= 126) || byte >= 128) {
                            consecutiveValid++;
                        } else {
                            startPos = i + 1;
                            break;
                        }
                    }
                    
                    // 还要确保 startPos 是个有意义的起点（最好是数字开头）
                    // 往前找到第一个数字或字母
                    for (let i = startPos; i < m3u8Pos; i++) {
                        const byte = decoded[i];
                        if ((byte >= 48 && byte <= 57) ||   // 数字
                            (byte >= 97 && byte <= 122) || // 小写字母
                            (byte >= 65 && byte <= 90)) {  // 大写字母
                            startPos = i;
                            break;
                        }
                    }
                    
                    // 现在提取从 startPos 到 m3u8Pos + 5（包含 .m3u8）
                    const pathBytes = decoded.slice(startPos, m3u8Pos + 5);
                    const cleanPath = pathBytes.toString('utf8');
                    
                    return 'https://play.svip30.tv/' + cleanPath;
                }
            } catch (e) {
                // 忽略
            }
        }
        return null;
    } catch (e) {
        return null;
    }
}

// 测试电视剧
console.log('=== 测试电视剧解密 ===');
var tvUrl = 'aFHBRI09c7H3M16HLeyl9l2oLWmrNokhbdm0x862M4jJI3u4Y7289Zt0L8zDIewSM0jUxMjEyLzI2OTk5XzI5NjM5M2Y0L2luZGV4Lm0zdTgO0O0O';
var result1 = decryptVideoUrl(tvUrl);
console.log(result1);

// 测试电影
console.log('\n=== 测试电影解密 ===');
var movieUrl = 'aFHBRI09c7H3M16HLeyl9l2oLWmrNokhMdT0I8z2c4GJF3u4L7m8NZu0Y8zDEe4SN0TMwMzIxLzUzNTdfNTQ1YjRhMDYv5Zu+5bqm5a+G56CBLm0zdTgO0O0O';
var result2 = decryptVideoUrl(movieUrl);
console.log(result2);
