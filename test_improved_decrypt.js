// 完善的解密函数
function decryptVideoUrl(encryptedUrl) {
    try {
        for (let offset = 1; offset < 20; offset++) {
            try {
                const testStr = encryptedUrl.substring(offset);
                const decoded = Buffer.from(testStr, 'base64').toString('utf8');
                
                if (decoded.includes('.m3u8')) {
                    // 找到 .m3u8 的位置
                    const m3u8Pos = decoded.indexOf('.m3u8');
                    
                    // 从后往前找最近的 / 或数字开始的位置，作为路径起点
                    let startPos = -1;
                    for (let i = m3u8Pos; i >= 0; i--) {
                        const charCode = decoded.charCodeAt(i);
                        // 如果是路径分隔符 /，或者是数字（通常是目录开始），并且之前的字符有乱码
                        if (decoded[i] === '/' && i > 0) {
                            // 检查这个位置之前是否有乱码
                            let hasJunk = false;
                            for (let j = Math.max(0, i - 10); j < i; j++) {
                                const code = decoded.charCodeAt(j);
                                if (code < 32 || (code > 126 && code !== 65279)) {
                                    hasJunk = true;
                                    break;
                                }
                            }
                            if (hasJunk) {
                                startPos = i + 1;
                                break;
                            }
                        }
                        // 如果是数字字符，并且前面有明显的乱码
                        if (i > 20 && decoded[i] >= '0' && decoded[i] <= '9') {
                            let hasJunk = false;
                            for (let j = Math.max(0, i - 20); j < i; j++) {
                                const code = decoded.charCodeAt(j);
                                if (code < 32 || code > 126) {
                                    hasJunk = true;
                                    break;
                                }
                            }
                            if (hasJunk) {
                                startPos = i;
                                break;
                            }
                        }
                    }
                    
                    // 如果没找到起点，尝试找第一个看起来正常的路径
                    if (startPos === -1) {
                        for (let i = 0; i < m3u8Pos; i++) {
                            const charCode = decoded.charCodeAt(i);
                            // 找看起来正常的ASCII字符开始的位置
                            if ((charCode >= 48 && charCode <= 57) || 
                                (charCode >= 97 && charCode <= 122) || 
                                (charCode >= 65 && charCode <= 90)) {
                                // 检查这个位置后面的20个字符是否大部分正常
                                let validCount = 0;
                                for (let j = i; j < Math.min(i + 20, decoded.length); j++) {
                                    const c = decoded.charCodeAt(j);
                                    if (c >= 32 && c <= 126) validCount++;
                                }
                                if (validCount >= 15) {
                                    startPos = i;
                                    break;
                                }
                            }
                        }
                    }
                    
                    if (startPos !== -1) {
                        // 提取从 startPos 到 .m3u8 + 5 的字符串
                        let path = decoded.substring(startPos, m3u8Pos + 5);
                        
                        // 清理掉任何乱码字符
                        let cleanPath = '';
                        for (let i = 0; i < path.length; i++) {
                            const c = path.charCodeAt(i);
                            // 只保留正常的ASCII字符、汉字和常见的路径字符
                            if ((c >= 32 && c <= 126) || (c >= 128 && c <= 65535)) {
                                cleanPath += path[i];
                            } else {
                                break;
                            }
                        }
                        
                        // 确保路径以数字或字母开头
                        const firstChar = cleanPath[0];
                        if (firstChar && !((firstChar >= '0' && firstChar <= '9') || 
                                          (firstChar >= 'a' && firstChar <= 'z') || 
                                          (firstChar >= 'A' && firstChar <= 'Z'))) {
                            const firstValidPos = cleanPath.search(/[0-9a-zA-Z]/);
                            if (firstValidPos !== -1) {
                                cleanPath = cleanPath.substring(firstValidPos);
                            }
                        }
                        
                        if (cleanPath.length > 0) {
                            return 'https://play.svip30.tv/' + cleanPath;
                        }
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
