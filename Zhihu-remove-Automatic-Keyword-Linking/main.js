// ==UserScript==
// @name         知乎-移除自动关键字链接
// @namespace    http://tampermonkey.net/
// @version      1.2
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
  
  // 目标链接特征（匹配自动生成的知乎站内链接）
  const TARGET_LINK_REGEX = /https:\/\/zhida\.zhihu\.com\/search\?.*?(content_id|q)=/i;

  // 防抖函数，避免频繁执行导致卡顿
  function debounce(func, wait = 100) {
    let timeout;
    return function(...args) {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }

  // 核心处理函数：安全转纯文本，不破坏React DOM结构
  function removeAutoLinks() {
    document.querySelectorAll('a[href]').forEach(link => {
      // 只处理符合规则的链接
      if (!TARGET_LINK_REGEX.test(link.href)) return;

      // 1. 提取纯文本内容（自动过滤svg、标签，只保留文字）
      const pureText = link.textContent.trim();
      
      // 2. 核心安全操作：仅修改a标签内部内容，保留a标签本身（React不会崩溃）
      link.innerHTML = pureText;

      // 3. 彻底禁用链接功能
      link.href = 'javascript:void(0)';
      link.style.pointerEvents = 'none';
      link.style.color = 'inherit';
      link.style.textDecoration = 'none';
      link.style.cursor = 'text';

      // 4. 清理所有影响复制、埋点的属性
      link.removeAttribute('target');
      link.removeAttribute('data-paste-text');
      link.removeAttribute('data-za-not-track-link');
      link.removeAttribute('data-za-detail-view-path');
      link.removeAttribute('data-highlight-id');
      link.removeAttribute('data-highlight-split-type');
      link.removeAttribute('data-highlight-id-extra');
    });
  }

  // 防抖执行，避免频繁DOM操作
  const debounceRemoveLinks = debounce(removeAutoLinks);

  // 初始执行
  removeAutoLinks();

  // 监听动态内容（评论区、无限滚动、折叠展开）
  const observer = new MutationObserver(debounceRemoveLinks);
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });

  // 监听SPA页面切换
  window.addEventListener('popstate', debounceRemoveLinks);
  window.addEventListener('pushstate', debounceRemoveLinks);

})();