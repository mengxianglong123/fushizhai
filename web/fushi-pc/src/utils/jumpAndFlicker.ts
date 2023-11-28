//使用onClick事件调用即可 target 为滚动目标对象的id
export  default (target:string){
    //找到对应组件 若存在执行滚动
    let anchorElement = document.getElementById(`${target}`);
    // behavior 定义滚动动画，默认值为auto。
    //   auto :没有动画直接跳转到对应处
    //   smooth: 有动画 平滑的滚动到对应处
    // block 定义垂直方向的对齐 默认值为start.
    //   start，表示顶端对齐。
    //   center，表示中间对齐。
    //   end，表示底端对齐。
    //   nearest：
    //      如果元素完全在视口内，则垂直方向不发生滚动。
    //      如果元素未能完全在视口内，则根据最短滚动距离原则，垂直方向滚动父级容器，使元素完全在视口内。
    // inline 定义水平方向的对齐，默认值为nearest。
    //   参数同 bloack 显然 start end 分别变更为左端右端
    if (anchorElement) {
        anchorElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
            inline :'start'
        });
    }
};