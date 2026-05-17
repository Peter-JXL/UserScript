// ==UserScript==
// @name         知乎-移除自动关键字链接
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  禁用知乎自动添加的关键字超链接（如 zhida.zhihu.com 链接）
// @icon         https://s21.ax1x.com/2025/03/23/pE0qpRK.jpg
// @compatible   chrome,edge,firefox
// @author       PeterJXL
// @homepageURL  https://www.peterjxl.com
// @license      MIT
// @create       2025-03-28
// @lastmodified 2026-05-17
// @match        https://www.zhihu.com/*
// @match        https://zhuanlan.zhihu.com/*
// @run-at       document-end
// @supportURL   https://github.com/Peter-JXL/UserScript/issues
// @grant        GM_addStyle
// ==/UserScript==

(function () {
   'use strict';

   /**
    * 目标链接：
    * https://zhida.zhihu.com/search?...content_id=...
    * https://zhida.zhihu.com/search?...q=...
    */
   const TARGET_SELECTOR =
       'a[href*="zhida.zhihu.com/search"]';

   /**
    * 纯 CSS 方案（最稳定）
    *
    * 不删除 DOM
    * 不替换节点
    * 不破坏 React
    */
   GM_addStyle(`
       ${TARGET_SELECTOR} {
           color: inherit !important;
           text-decoration: none !important;
           cursor: text !important;
           pointer-events: none !important;
       }
   `);

   /**
    * 补充保险：
    * 有些情况下知乎会动态恢复 pointer-events
    * 所以这里再做一次 JS 层处理
    */
   function processLink(link) {

       // 防止重复处理
       if (link.dataset.zhihuAutoLinkDisabled) {
           return;
       }

       link.dataset.zhihuAutoLinkDisabled = '1';

       // 去掉 href（但保留 DOM 节点）
       link.removeAttribute('href');

       // 阻止点击
       link.addEventListener('click', e => {
           e.preventDefault();
           e.stopPropagation();
       }, true);
   }

   function processNode(node) {

       if (node.nodeType !== Node.ELEMENT_NODE) {
           return;
       }

       // 自己就是链接
       if (node.matches?.(TARGET_SELECTOR)) {
           processLink(node);
       }

       // 子元素中的链接
       node.querySelectorAll?.(TARGET_SELECTOR)
           .forEach(processLink);
   }

   /**
    * 初始处理
    */
   processNode(document.body);

   /**
    * 监听动态内容
    *
    * 只处理新增节点
    * 避免全页面 querySelectorAll 带来的性能问题
    */
   const observer = new MutationObserver(mutations => {
       for (const mutation of mutations) {
           for (const node of mutation.addedNodes) {
               processNode(node);
           }
       }
   });

   observer.observe(document.body, {
       childList: true,
       subtree: true
   });
})();