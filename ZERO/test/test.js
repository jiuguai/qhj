    $("thead>tr>th:nth-child(6)").after("<th>下级用户数</th>")


    $("tbody>tr>td:nth-child(6)").after("<td></td>")




    $("tbody>tr").each(function(k, v) {
        var url = /\/.+?\d+.html/.exec($(v).find('td>button').eq(0).attr("onclick"))[0];
        var td = $(v).find('td').eq(6)
        $.ajax({
            url: url,
            success: function(result) {
                var vitual = $("<div></div>").html(result)
                var tbody = vitual.find('.x-body:nth-last-child(1)');
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
                td.find('table').css({ "width": "90px", "height": "60px", "padding": 0, "text-align": "right" })
                td.find('td').css({ "width": "50px", "border-width": "0px 0px 1px" })
                td.find('tbody>tr>td:nth-child(1)').css({ "padding": "2px 0px" })
                td.find('tbody>tr>td:nth-child(2)').css({ "color": "red", "padding": "0px" })
            }
        })
    });



    $.get("/admin/user/lower_level_user/user_id/1.html", function(result) {
        var vitual = $("<div></div>").html(result)
        var tbody = vitual.find('.x-body:nth-last-child(1)');
        console.log(tbody)
    })


        // old

        var url_flag
        if (window.location.pathname.match(/admin\/user\/lower_level_user\/user_id/) != null) {
            url_flag = "用户下级名单"
        }
        console.log(document.cookie);
        switch (url_flag) {
            case "用户下级名单":
                var tbody = $('.x-body:nth-last-child(1)');
                var trs = tbody.find('tbody>tr');
                var total = trs.length;
                var info = tbody.find('span[class="x-right"]');
                var info_map = {
                    "白户": 0,
                    "vip": 0,
                    "vvip": 0,
                };
                trs.each(function(k, v) {
                    var state = $(v).find('td:nth-child(3)').text();
                    // console.log(state);
                    info_map[state] += 1;

                });


                info.html(`共有下级用户:${total} <br>
                       VVIP:<strong style="color:red">${info_map["vvip"]}</strong>&nbsp;&nbsp;
                       VIP:<strong style="color:red">${info_map["vip"]}</strong>&nbsp;&nbsp;
                       白户:<strong style="color:red">${info_map["白户"]}</strong>`);
                break;

        }