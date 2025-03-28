// ==UserScript==
// @name         知乎-移除自动关键字链接
// @namespace    https://github.com/Peter-JXL/UserScript
// @version      1.0
// @description  移除知乎自动添加的关键字超链接（如 zhida.zhihu.com 链接）
// @author       PeterJXL
// @match        https://www.zhihu.com/*
// @match        https://zhuanlan.zhihu.com/*
// @grant        none
// @run-at       document-end
// ==/UserScript==


(function() {
  'use strict';

  // 目标链接特征（匹配自动生成的知乎站内链接）
  const TARGET_LINK_REGEX = /https:\/\/zhida\.zhihu\.com\/search\?.*?(content_id|q)=/i;

  // 主处理函数
  function removeAutoLinks() {
      // 查找所有包含目标链接的 <a> 标签
      document.querySelectorAll('a[href]').forEach(link => {
          if (TARGET_LINK_REGEX.test(link.href)) {
              // 创建替换的文本节点
              const textNode = document.createTextNode(link.textContent);
              // 用纯文本替换链接
              link.parentNode.replaceChild(textNode, link);
          }
      });
  }

  // 初始执行
  removeAutoLinks();

  // 监听动态内容（如评论区加载、无限滚动）
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

  // 监听知乎的异步加载（SPA页面切换）
  window.addEventListener('popstate', removeAutoLinks);
  window.addEventListener('pushstate', removeAutoLinks);

})();