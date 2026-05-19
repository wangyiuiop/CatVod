#!/usr/bin/env node
/**
 * Node.js 调用 WebAssembly 模块
 * 直接使用 build_play_url 函数
 */

const fs = require('fs');
const https = require('https');
const http = require('http');
const path = require('path');

// 下载并执行 WASM 模块
async function initWasm() {
    console.log('[+] 加载 WASM 模块...');
    
    // 动态导入 wasm-pack 生成的代码
    const wasmPath = path.join(__dirname, 'nbmovie_wasm_bg.wasm');
    const jsPath = path.join(__dirname, 'nbmovie_wasm.js');
    
    // 检查文件是否存在
    if (!fs.existsSync(wasmPath)) {
        console.error('[-] WASM 文件不存在');
        return null;
    }
    
    try {
        // 读取 WASM 文件
        const wasmBuffer = fs.readFileSync(wasmPath);
        
        // 创建一个简单的 WASM 实例化环境
        const importObject = {
            './nbmovie_wasm_bg.js': {
                '__wbg_now_16f0c993d5dd6c27': () => Date.now(),
                '__wbindgen_add_to_stack_pointer': (arg) => arg - 16,
            }
        };
        
        // 实例化 WASM (简化版本)
        const wasmModule = await WebAssembly.instantiate(wasmBuffer);
        
        console.log('[+] WASM 加载成功');
        console.log('[+] 可用导出函数:', Object.keys(wasmModule.instance.exports));
        
        return wasmModule.instance.exports;
    } catch (e) {
        console.error('[-] WASM 加载失败:', e.message);
        return null;
    }
}

// 获取播放页面
async function getPlayPage(url) {
    console.log('[+] 获取播放页面:', url);
    
    return new Promise((resolve, reject) => {
        https.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve(data));
        }).on('error', reject);
    });
}

// 提取页面参数
function extractParams(html) {
    const params = {};
    
    // 提取 dataid
    const dataidMatch = html.match(/dataid="([^"]+)"/);
    if (dataidMatch) params.dataid = dataidMatch[1];
    
    // 提取 vodid
    const vodidMatch = html.match(/var\s+vodid\s*=\s*['"]([^'"]+)['"]/);
    if (vodidMatch) params.vodid = vodidMatch[1];
    
    // 提取 meta#nb-st
    const nbStMatch = html.match(/<meta[^>]+id="nb-st"[^>]+content="([^"]+)"/);
    if (nbStMatch) params.timestamp = nbStMatch[1];
    
    return params;
}

// 调用视频播放 API
async function callPlayApi(baseUrl, params, wasmExports) {
    console.log('\n[+] 调用 build_play_url...');
    console.log('    dataid:', params.dataid);
    console.log('    vodid:', params.vodid);
    console.log('    quality:', params.quality || '1080');
    
    if (wasmExports && wasmExports.build_play_url) {
        try {
            // 调用 WASM 函数
            const result = wasmExports.build_play_url(
                params.dataid,
                params.secret_key || '',
                params.quality || '1080',
                params.play_key || ''
            );
            
            console.log('[+] build_play_url 返回:', result);
            return result;
        } catch (e) {
            console.error('[-] WASM 调用失败:', e.message);
        }
    } else {
        console.log('[-] build_play_url 函数不可用');
    }
    
    return null;
}

// 主函数
async function main() {
    const testUrl = 'https://www.4kvm.tv/play/ch44vpwk4';
    
    console.log('='.repeat(60));
    console.log('4kvm.tv WebAssembly 逆向工具');
    console.log('='.repeat(60));
    
    // 获取播放页面
    const html = await getPlayPage(testUrl);
    const params = extractParams(html);
    
    console.log('\n提取的参数:');
    console.log(JSON.stringify(params, null, 2));
    
    // 尝试加载 WASM
    const wasmExports = await initWasm();
    
    if (wasmExports) {
        // 尝试调用 build_play_url
        await callPlayApi(testUrl, params, wasmExports);
    } else {
        console.log('\n[!] 无法加载 WASM 模块');
        console.log('请确保 nbmovie_wasm_bg.wasm 文件存在');
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('说明：由于 WASM 需要完整的 JavaScript 运行时环境');
    console.log('建议使用 Playwright/Selenium 来获取真实的播放地址');
    console.log('='.repeat(60));
}

main().catch(console.error);
