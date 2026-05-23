// 改进版的解密函数 - 找真正干净的起始位置
function decryptVideoUrl(encryptedUrl) {
    try {
        for (let offset = 1; offset < 20; offset++) {
            try {
                const testStr = encryptedUrl.substring(offset);
                const decoded = Buffer.from(testStr, 'base64');
                
                // 找到有效路径开始的位置
                let startPos = -1;
                for (let i = 0; i < decoded.length; i++) {
                    // 首先检查这个字节是不是有效的起始字符
                    const firstByte = decoded[i];
                    if (!((firstByte >= 48 && firstByte <= 57) ||   // 数字
                          (firstByte >= 97 && firstByte <= 122) ||   // 小写字母
                          (firstByte >= 65 && firstByte <= 90))) {   // 大写字母
                        continue;
                    }
                    
                    // 现在检查从这个位置开始的连续40个字符，看看是否大部分都是有效的
                    let validCount = 0;
                    let hasSlash = false;
                    let hasM3u8 = false;
                    
                    for (let j = 0; j < Math.min(60, decoded.length - i); j++) {
                        const c = decoded[i + j];
                        if ((c >= 48 && c <= 57) ||   // 数字
                            (c >= 97 && c <= 122) ||   // 小写字母
                            (c >= 65 && c <= 90) ||    // 大写字母
                            c === 47 ||                // /
                            c === 95 ||                // _
                            c === 46 ||                // .
                            (c >= 128)) {              // 汉字
                            validCount++;
                        }
                        
                        if (c === 47) hasSlash = true;
                        
                        // 简单检查是否包含.m3u8的模式
                        if (j >= 4) {
                            const c1 = decoded[i + j - 4];
                            const c2 = decoded[i + j - 3];
                            const c3 = decoded[i + j - 2];
                            const c4 = decoded[i + j - 1];
                            const c5 = decoded[i + j];
                            if (c1 === 46 && c2 === 109 && c3 === 51 && c4 === 117 && c5 === 56) {
                                hasM3u8 = true;
                            }
                        }
                    }
                    
                    // 如果有足够多有效字符，且有/和.m3u8，那么就是这里
                    if (validCount >= 40 && hasSlash && hasM3u8) {
                        startPos = i;
                        break;
                    }
                }
                
                if (startPos !== -1) {
                    // 从startPos开始，提取到.m3u8+5的位置
                    const tempStr = decoded.toString('utf8', startPos);
                    const m3u8Pos = tempStr.indexOf('.m3u8');
                    if (m3u8Pos !== -1) {
                        const cleanPath = tempStr.substring(0, m3u8Pos + 5);
                        return 'https://play.svip30.tv/' + cleanPath;
                    }
                }
            } catch (e) {
                // 忽略错误继续尝试
            }
        }
        return null;
    } catch (e) {
        return null;
    }
}

// 测试综艺URL
var varietyUrl = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhbdH0o8t2Y42JR3u4M7T8IZu0Y82D9etSL0zIwMjMwMzIxLzYzOTNfMWU3MWM0MzEvaW5kZXgubTN1OAO0O0OO0O0O';
console.log('测试综艺URL...');
var result1 = decryptVideoUrl(varietyUrl);
console.log(result1);
console.log();

// 测试电影URL
var movieUrl = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhMdT0I8z2c4GJF3u4L7m8NZu0Y82D9e4tSL0zIwMjUwMzI1L2R5LzU0MzBfY2U1ZmJhZjgvWcOF5Lqn5bmg5pa55a6X5ZGY5LmL5Lia54K5Lm0zdTgO0O0O';
console.log('测试电影URL...');
var result2 = decryptVideoUrl(movieUrl);
console.log(result2);
