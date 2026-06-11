// ==UserScript==
// @name         知乎-移除自动关键字链接
// @namespace    http://tampermonkey.net/
// @version      1.3.2
// @description  移除知乎自动添加的关键字超链接（如 zhida.zhihu.com 链接）
// @icon         https://s21.ax1x.com/2025/03/23/pE0qpRK.jpg
// @compatible   chrome,edge,firefox
// @author       PeterJXL
// @homepageURL  https://www.peterjxl.com
// @license      MIT
// @create       2025-03-28
// @lastmodified  2026-05-17
// @match        https://www.zhihu.com/*
// @match        https://zhuanlan.zhihu.com/*
// @run-at       document-end
// @supportURL   https://github.com/Peter-JXL/UserScript/issues
// @grant        none
// ==/UserScript==

(function() {
  'use strict';

  // 仅匹配 zhida.zhihu.com 的搜索链接
  const TARGET_LINK_REGEX = /https:\/\/zhida\.zhihu\.com\/search\?.*/i;

  function removeAutoLinks() {
    document.querySelectorAll('a[href]').forEach(link => {
      if (!TARGET_LINK_REGEX.test(link.href)) return;
      if (link.dataset.done) return;
      link.dataset.done = "true";

      // 1. 获取父级 span
      const parentSpan = link.closest("span");
      if (!parentSpan) return;

      // 2. 提取纯文本
      const text = link.textContent.trim();
      if (!text) return;

      // 3. 清空 a 内部所有内容（文字 + svg 全部删掉）
      link.innerHTML = "";

      // 4. 把文本放到 span 最开头
      const textNode = document.createTextNode(text);
      parentSpan.prepend(textNode);

      // 5. 清空 href + 禁用点击
      link.setAttribute("href", "");
      link.style.pointerEvents = "none";
      link.style.color = "inherit";
      link.style.textDecoration = "none";
    });
  }

  removeAutoLinks();

  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.addedNodes.length) {
        removeAutoLinks();
      }
    });
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });

  window.addEventListener('popstate', removeAutoLinks);
  window.addEventListener('pushstate', removeAutoLinks);

})();