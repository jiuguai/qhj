// ==UserScript==
// @name         QIHUOJU
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       ZERO
// @match        https://app0001.yrapps.cn*
// @grant        none
// @require      https://cdn.staticfile.org/jquery/3.4.1/jquery.min.js
// ==/UserScript==

(function() {
    'use strict';

    var path = location.pathname;


    switch(path){

        case "/admin/Good/goodList":
            goods_list()
            break;
        case "/admin/User/userMemberList":
            user_member_list()
            break
        case "/admin/Free/freeList":
            goods_list()
            break
    }

    function goods_list(){
        $("thead>tr>th:nth-child(2)").after("<th>goods_id</th>")

        $("tbody>tr>td:nth-child(2)").after("<td></td>")
        $("tbody>tr>td:nth-child(2)").each(function(k, td){
            var $td = $(td);
            $td.next().html(`<div style="color:red;align:right;font-size;15px">
${$td.find('img,button').attr('goods_id')}
</div>
`

            )

        })
        $("tbody>tr>td:nth-child(3)").css({'text-align':'right','font-size':16})

    }




    function user_member_list(){
        $("thead>tr>th:nth-child(6)").after("<th>下级用户数</th>")


        $("tbody>tr>td:nth-child(6)").after("<td></td>")


        $("tbody>tr").each(function(k, v) {
            var url = /\/.+?\d+.html/.exec($(v).find('td>button').eq(0).attr("onclick"))[0];
            var td = $(v).find('td').eq(6)
            $.ajax({
                url:url,
                success:function(result) {
                    var vitual = $("<div></div>").html(result)
                    var tbody =vitual.find('.x-body:nth-last-child(1)');
                    var trs = tbody.find('tbody>tr');
                    var total = trs.length;

                    var info_map = {
                        "白户": 0,
                        "vip": 0,
                        "vvip": 0,
                    };
                    trs.each(function(k, v) {
                        var state = $(v).find('td:nth-child(3)').text();
                        // console.log(state);
                        // console.log(state)
                        info_map[state] += 1;

                    });


                    td.html(`<div><table ><tbody>
<tr>
<td>VVIP：</td>
<td>${info_map["vvip"]}</td>
</tr>
<tr>
<td>VIP：</td>
<td>${info_map["vip"]}</td>
</tr>
<tr>
<td>白户：</td>
<td>${info_map["白户"]}</td>
</tr>
<tr>
<td>合计：</td>
<td>${total} </td>
</tr>

</tbody></table></div>`);
                    td.find('table').css({"width":"90px","height":"40px","padding":0,"text-align":"right"})
                    td.find('td').css({"width":"50px","border-width":"0px 0px 1px"})
                    td.find('tbody>tr>td:nth-child(1)').css({"padding":"2px 0px"})
                    td.find('tbody>tr>td:nth-child(2)').css({"color":"red","padding":"0px"})
                }
            })
        });

    };
    

    // Your code here...
})();