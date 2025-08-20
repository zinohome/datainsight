(function() {
    function smoothAutoScroll(container, options) {
        let rowHeight = parseInt(options.rowHeight) || 40;
        let visibleRows = parseInt(options.visibleRows) || 10;
        let scrollInterval = parseInt(options.scrollInterval) || 1000;
        let paused = false;
        let frameDuration = 16; // 约60fps
        let distancePerFrame = rowHeight / (scrollInterval / frameDuration);
        let targetScrollTop = 0;
        let acc = 0;
        function step() {
            if (paused) return;
            let maxScroll = container.scrollHeight - container.clientHeight;
            if (Math.abs(container.scrollTop - targetScrollTop) < 1) {
                targetScrollTop += rowHeight;
                if (targetScrollTop > maxScroll + 1) {
                    targetScrollTop = 0;
                    container.scrollTop = 0;
                }
            }
            let delta = targetScrollTop - container.scrollTop;
            acc += Math.sign(delta) * Math.min(Math.abs(delta), distancePerFrame);
            if (Math.abs(acc) >= 1) {
                let move = Math.trunc(acc);
                container.scrollTop += move;
                acc -= move;
            }
            requestAnimationFrame(step);
        }
        container.addEventListener('mouseenter', ()=>{paused = true;});
        container.addEventListener('mouseleave', ()=>{
            if(!paused) return;
            paused = false; requestAnimationFrame(step);
        });
        requestAnimationFrame(step);
    }
    function bindAllScrollTables() {
        document.querySelectorAll('[data-scroll-table]').forEach(function(container){
            if(container.dataset.scrollBinded) return;
            container.dataset.scrollBinded = '1';
            smoothAutoScroll(container, {
                rowHeight: container.dataset.rowHeight,
                visibleRows: container.dataset.visibleRows,
                scrollInterval: container.dataset.scrollInterval
            });
        });
    }
    if(document.readyState === 'complete'){
        bindAllScrollTables();
    }else{
        window.addEventListener('DOMContentLoaded', bindAllScrollTables);
        window.addEventListener('load', bindAllScrollTables);
    }
    setInterval(bindAllScrollTables, 3000);
})();