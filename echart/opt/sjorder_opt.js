myChart = echarts.init(document.getElementById('main'), 'dark');
myChart_detail = echarts.init(document.getElementById('main_abut'), 'dark');
// myChart_detail = echarts.init(document.getElementById('main_order_detail'), 'dark');
myChart_goods = echarts.init(document.getElementById('main_pie_goods'), 'dark');

var goods_option = function() {
    var order_counts = 0
    var goods_legend = []
    order_data['goods_order'].forEach(function(item) {
        order_counts += item['value']
        goods_legend.push(item['name'])
    })
    
    var option = {
        title: {
            text: '三金商品占比',
            left: 'left',
            subtext: `订单数:${order_counts}`
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)",
            textStyle:{
                align:'left'
            }
        },
        calculable:true,
        legend: {
            // type: 'scroll',
            orient: 'vertical',
            right: 0,
            top: 20,
            bottom: 20,
            data: goods_legend,

            // selected: data.selected
        },

        series: [{
            name: '三金商品',
            type: 'pie',
            radius: '50%',
            center: ['40%', '50%'],
            data: order_data['goods_order'],

            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            },
            label: {
                    align:'right',
                    formatter: `{b}: {@2012} \n({d}%)`
            },
        }]
    };
    console.log(option)
    return option
}()


var wait_option = function() {
    var legend_names = []
    var data = []
    var xaxis_data = order_data['xaxis']
    console.log(order_data)

    colors = {'已回复':'#dd6b66',
               "未回复":'#759aa0'}
    order_data['abut_data'].forEach(function(v) {
        
         // console.log(v)
        legend_names.push(v['name']);
        data.push({
            // '#dd6b66','#759aa0','#e69d87'
            itemStyle:{
                color:colors[v['name']],
            },
    
            name: v['name'],
            type: 'bar',
            stack: 'all',
            label: {
                normal: {
                    show: true,
                    position: "insideTopRight",
                    // offset: [5, 0],
                    formatter: function(item) {

                        value = item['value'] === 0 ? "" : item['value']
                        return value
                    }
                }
            },
            // itemStyle:{
            //     color:"#FF0000"
            // },
            data: v['data']
        })
    });
    data.push({
        // '#dd6b66','#759aa0','#e69d87'
        itemStyle:{
            color:'#e69d87',
        },
        name: order_data['order_data']['name'],
        type: 'line',
        data: order_data['order_data']['data'],
        label: {
            normal: {
                show: true,
                // position: "insideLeft",
                // offset:[15,0],
                formatter: function(item) {
                    value = item['value'] === 0 ? "" : item['value']
                    return value
                }
            }
        },
    })
    // 将下单数 前置与
    legend_names.unshift(order_data['order_data']['name'])


    // 主option
    var option = {
        title: {
            text: '已对接待回复'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            },
            textStyle:{

                align:'left'

            },
            formatter: function(item) {
                // name: "2019-12-18"
                // console.log(item)
                cur_order_count = order_data['cur_date'][item[0]['name']]
                not_cur_order_count = order_data['ncur_date'][item[0]['name']]



                var total = cur_order_count + not_cur_order_count
                var temp = ""

                item.forEach(function(v) {
                    
                    series_name = v['seriesName']
                    temp += v['marker'] + series_name +
                        "：" + v['value'] + "</br>"

                })
                temp = item[0]['name'] +
                    "</br>" +
                    `对接：${cur_order_count}C + ${not_cur_order_count} = ${total}</br>` +
                    temp

                return temp
            }
        },

        dataZoom: [

            {
                type: 'inside',
                xAxisIndex: [0],

                show: true,
                start: 35,
                end: 100
            },
            {
                bottom: 0,
                // textStyle: {
                //     color: '#8392A5'
                // },
                // handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                // handleSize: '80%',
                dataBackground: {
                    areaStyle: {
                        color: '#8392A5'
                    },
                    lineStyle: {
                        opacity: 0.8,
                        color: '#8392A5'
                    }
                },
                // handleStyle: {
                //     color: '#fff',
                //     shadowBlur: 3,
                //     shadowColor: 'rgba(0, 0, 0, 0.6)',
                //     shadowOffsetX: 2,
                //     shadowOffsetY: 2
                // }
            },


        ],

        legend: {
            data: legend_names
        },

        toolbox: {
            show: true,
            left: "80%",
            // orient:"vertical",
            feature: {

                dataZoom: {
                    yAxisIndex: 'none'
                },
                // dataView: {readOnly: false},
                magicType: { type: ['line', 'bar'] },
                restore: {},
                saveAsImage: {}
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',

            data: xaxis_data,
            axisLabel: {
                rotate: 45,
                formatter: function(value, index) {
                    var day = "星期" + "日一二三四五六".charAt(new Date(value).getDay())
                    // console.log(value)
                    return value + "\n" + day
                }
            }


        },
        yAxis: {
            type: 'value'
        },
        series: data
    };
    console.log(option)
    return option
}()

// 点击opthin
myChart.on('click', function(item) {
    console.log(item)
    // name: "2019-12-20"
    var abut_details = order_data['abut_details'][item['name']]
    var order_details = order_data['order_details'][item['name']]
    
    goods_keys = new Set(Object.keys(order_details))
    Object.keys(abut_details).forEach(function(goods_name){
        goods_keys.add(goods_name)
    })
    x_data = []
    for (let f of goods_keys){x_data.push(f)}

    var p_orders = []
    var recv=[]
    var wrecv=[]
    var legend_names = []
    console.log(abut_details)
    console.log(order_details)
    x_data.forEach(function(key){
                // '#dd6b66','#759aa0','#e69d87'
        // itemStyle:{
                //     color:'#759aa0',
                // }
        // 
        series = []
        p_orders.push( order_details.hasOwnProperty(key)?order_details[key]['下单数']:0)
        series.push( {
                name:'下单数',
                type:'line',
                barWidth: '60%',
                data:p_orders,
                itemStyle:{
                    color:'#e69d87',
                },
                label: {
                    normal: {
                        show: true,
                        // position: "insideTopRight",
                        // offset: [5, 0],
                        formatter: function(item) {

                            value = item['value'] === 0 ? "" : item['value']
                            return value
                        }
                    }
                },
        })

        recv.push(abut_details.hasOwnProperty(key) && abut_details[key].hasOwnProperty('已回复') ?abut_details[key]['已回复']:0)
        series.push( {

                // '#dd6b66','#759aa0','#e69d87'
                itemStyle:{
                    color:'#dd6b66',
                },
                name:'已回复',
                type:'bar',
                barWidth: '60%',
                stack:"abut",
                data:recv,

                label: {
                    normal: {
                        show: true,
                        position: "insideTopRight",
                        // offset: [5, 0],
                        formatter: function(item) {

                            value = item['value'] === 0 ? "" : item['value']
                            return value
                        }
                    }
                },
        })

        wrecv.push(abut_details.hasOwnProperty(key) && abut_details[key].hasOwnProperty('待回复') ?abut_details[key]['待回复']:0)
        series.push( {
                // '#dd6b66','#759aa0','#e69d87'
                itemStyle:{
                    color:'#759aa0',
                },
                name:'待回复',
                type:'bar',
                barWidth: '60%',
                stack:"abut",
                data:wrecv,
                label: {
                    normal: {
                        show: true,
                        position: "insideTopRight",
                        // offset: [5, 0],
                        formatter: function(item) {

                            value = item['value'] === 0 ? "" : item['value']
                            return value
                        }
                    }
                },
        })
        recv.forEach(function(v){
            if(v!==0){
                legend_names.push('已回复');
        
            }
        })
        wrecv.forEach(function(v){
            if(v!==0){
                legend_names.push('待回复')
         
            }
        })


    })



    var option = {
        legend: {
            // type: 'scroll',
            // orient: 'vertical',
            right: 0,
            top: 20,
            bottom: 20,
            data: legend_names,

            // selected: data.selected
        },

        tooltip : {
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            },
            textStyle:{

                align:'left'

            },
            formatter: function(item) {
                // name: "2019-12-18"
                // console.log(item)
                var key = item[0]['name']
                cur_order_count = abut_details.hasOwnProperty(key) && abut_details[key].hasOwnProperty('当日') ?abut_details[key]['当日']:0
                not_cur_order_count = abut_details.hasOwnProperty(key) && abut_details[key].hasOwnProperty('非当日') ?abut_details[key]['非当日']:0
                console.log()

                var total = cur_order_count + not_cur_order_count
                var temp = ""
                item.forEach(function(v) {
                    series_name = v['seriesName']
                    temp += `${v['marker']} ${series_name}
                        ： ${v['value']} </br>`

                })
                temp = item[0]['name'] +
                    "</br>" +
                    `对接：${cur_order_count}C + ${not_cur_order_count} = ${total}</br>` +
                    temp

                return temp
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true,
            // top:10
        },
        xAxis : [
            {
                type : 'category',
                data : x_data ,
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : series
    };
    myChart_detail.setOption(option);




})



myChart_goods.on('legendselectchanged',function(e){

    var order_counts = 0
    var goods_legend = []
    order_data['goods_order'].forEach(function(item) {

        if(e.selected[item.name]){
            order_counts += item['value']
        }  
    });
    myChart_goods.setOption({
        title: {
            subtext: `订单数:${order_counts}`
        }})
})



