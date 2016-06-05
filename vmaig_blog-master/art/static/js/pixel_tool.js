/**
 * Created by Administrator on 2016/6/1 0001.
 */

    function GetDom(x){return document.getElementById(x);}

    function getPagePos(el){
     var x=y=0;
     while(el){ x+=el.offsetLeft; y+=el.offsetTop; el=el.offsetParent;}
     return {x:x,y:y}
    }

    //设置调色盘
    var colorPanel = function(){
        var tb, c, s = "" , cp = "ColorPanel";
        var colors = "00,33,66,99,cc,ff".split(",");
        return {
            el : null,
            setColor : function(el){
                var o = GetDom(el);
                o.onfocus = function(){
                    colorPanel.el = o;
                    if(!tb){
                        tb = document.createElement("div");
                        tb.id = "ColorPanel";
                        for(var x=0; x<6; x++){
                            s += '<tr>';
                            for(var y=0; y<6; y++){
                                for(var z=0; z<6; z++){
                                    c = colors[x] + colors[y] + colors[z];
                                    s += '<td color="#'+ c +'" ></td>'
                                }
                            }
                                s += '</tr>';
                        }
                        tb.innerHTML = "<table id='tb'>" + s + "</table>";
                        document.body.appendChild(tb);
                        tb.style.position = "absolute";
                        colorPanel.setPos(tb,o);
                        var td = tb.getElementsByTagName("td");
                        for(var i=0;i<td.length;i++){
                            td[i].onclick = function(){
                                colorPanel.hide();
                                iconTable.setColor( this.getAttribute("color") );
                            }
                            td[i].onmouseover = function(){ colorPanel.showColor(this);}
                        }
                    }
                    else{
                    GetDom(cp).style.display = "block";
                    colorPanel.setPos(tb,o);
                    }

                }

            },
            showColor : function(el){
                colorPanel.el.style.backgroundColor = el.getAttribute("color");
                GetDom("colorBar").value = el.getAttribute("color");
            },

            hide : function(){ GetDom(cp).style.display = "none"; },

            setPos : function(tb,el){ //设置调色板位置
                tb.style.left = getPagePos(el).x + "px";
                tb.style.top  = getPagePos(el).y + el.offsetHeight + 1 + "px";
            }
        }
    }()

    //画板表格
    var iconTable = {
        curColor : "#FF0000",//当前颜色值
        box : GetDom("box"), //画板表格的容器
        nav : GetDom("nav"), //画板表格的容器
        border : "none",
        l : 50, //格子数 l * l
        wh_default : 11,//格子初始宽高度,
        wh : 11, //格子宽高度,
        MaxWH : 16,
        MinWH : 4,
        ColorHash : null,
        init : function(l){ //利用数组拼接表格字符
            this.l = l || 50;
            var l = this.l;
            var aT = ["<table id='iTable'>"];
            var td_id = 0;
            for(var x=0,t=this.l; x<t; x++){
                aT.push("<tr>");
                for(var y=0,y1=this.l; y<y1; y++){
                    aT.push("<td id='"+td_id+"'></td>");
                    td_id++;
                }
                aT.push("</tr>");
            }
            aT.push("</table>");
            //将table写到容器里
            this.box.innerHTML = aT.join("");
            this.resetPos(); //画布居中
            iconTable.border = "none";
            GetDom("done").value = "隐藏边框";
            iconTable.wh = iconTable.wh_default ;
            var td = GetDom("iTable").getElementsByTagName("td");

            this.ColorHash = new Array(l*l);


            //初始化导航table
            var navT = ["<table id='navTable'>"];
            var nav_td_id = 0;
            for(var x=0,t=this.l; x<t; x++){
                navT.push("<tr>");
                for(var y=0,y1=this.l; y<y1; y++){
                    navT.push("<td id='nav_"+nav_td_id+"'></td>");
                    nav_td_id++;
                }
                navT.push("</tr>");
            }
            navT.push("</table>");
            this.nav.innerHTML = navT.join("");


           //遍历第一个表格,并注册事件
            for(var i=0,l=td.length; i<l; i++){
                (function(k){
                    td[k].onclick = function(){
                        this.style.backgroundColor = iconTable.curColor;
                        iconTable.ColorHash[k] = iconTable.curColor;

                        //nav 随之变化
                        GetDom("nav_"+this.id).style.backgroundColor = iconTable.curColor;
                    }
                    td[k].onmouseover = function(e){
                        var e = e || window.event;
                        if(e.ctrlKey ){
                            this.style.backgroundColor = iconTable.curColor;
                            iconTable.ColorHash[k] = iconTable.curColor;

                            //nav 随之变化
                            GetDom("nav_"+this.id).style.backgroundColor = iconTable.curColor;
                        }
                    }
                })(i);
            }
        },
        //设置当前颜色
        setColor : function(x){ this.curColor = x; },

        removeBorder : function(){
            var td = GetDom("iTable").getElementsByTagName("td");
            var b = iconTable.border;
            for(var i=0,l=td.length; i<l; i++){
                td[i].style.border = b;
            }
            iconTable.border = (iconTable.border == "none")?"1px solid #999": "none";
            GetDom("done").value = (iconTable.border == "none")?"隐藏边框":"显示边框";
         },

        clear : function(){
            var td = GetDom("iTable").getElementsByTagName("td");
            for(var i=0,l=td.length; i<l; i++){
                td[i].style.backgroundColor = "#fff";
            }
        },


        //画布居中
        resetPos : function(){
            var w = GetDom("iTable").offsetWidth;
            var bW = GetDom("main").offsetWidth;
            var l = (bW-w) / 2;
            GetDom("box").style.marginLeft = l + "px";


        },





        sizeChange : function(pos){
            var pos = pos || 1;
            var td = GetDom("iTable").getElementsByTagName("td");
            var tmp = this.wh + ( 1 * pos );
            if( tmp <= this.MaxWH && tmp >= this.MinWH ){ this.wh = tmp; }
            for(var i=0,l=td.length; i<l; i++){
                td[i].style.height = td[i].style.width = this.wh + "px";
            }
            iconTable.resetPos();
        },

        numChange : function(l){
            GetDom("iTable").parentNode.removeChild( GetDom("iTable") );
            iconTable.init(l);
            iconTable.resetPos();
        },

        showHash : function(){
            GetDom("HashInfo").value = iconTable.ColorHash ;
        },

        submitColor : function(v){
            var td = GetDom("iTable").getElementsByTagName("td");
            var arr = iconTable.ColorHash = v.split(",");
            console.log(td.length)
            for(var i=0,l=td.length; i<l; i++){

                if ( i == 2488)
                    td[i].style.backgroundColor = arr[i];
                td[i].style.backgroundColor = arr[i];
            }

            var td = GetDom("navTable").getElementsByTagName("td");
            var arr = iconTable.ColorHash = v.split(",");
            console.log(td.length)
            for(var i=0,l=td.length; i<l; i++){

                if ( i == 2488)
                    td[i].style.backgroundColor = arr[i];
                td[i].style.backgroundColor = arr[i];
            }
        }

    }
    iconTable.init();
    colorPanel.setColor("colorBar");
    GetDom("done").onclick = function(){ iconTable.removeBorder(); }
    GetDom("clear").onclick = function(){ iconTable.clear(); }
    GetDom("bigger").onclick = function(){ iconTable.sizeChange(1); }
    GetDom("smaller").onclick = function(){ iconTable.sizeChange(-1); }
    GetDom("ColorInfo").onclick = function(){ iconTable.showHash(); }
    GetDom("SubmitColor").onclick = function(){ iconTable.submitColor(GetDom("HashInfo").value);}

    GetDom("color_choose").onclick = function(){ iconTable.setColor( GetDom("color_prepare").value ); }
