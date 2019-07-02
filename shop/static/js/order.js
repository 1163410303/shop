	$(document).ready(function(){
	 $(".tabs").slide({ trigger: "click" });

});
function delete_order(id){
			$.post(
			'/delete_order/',{
				"id" : id
				},
			function (data){
				if(data) {
                    alert('删除成功')
                    top.location.reload()
                }
			});
}
function edit_order(id) {
    var text = prompt("请输入更改后的数据", "商品ID+商品名+数量+售价+用户名+地址+日期+备注"); //将输入的内容赋给变量
    if (text == "商品ID+商品名+数量+售价+用户名+地址+日期+备注") {
        alert('您没有做出任何更改')
    }
    else {
        var edit_args = text.split('+');
        if (text)//如果返回的有内容
        {
            if (edit_args.length == 8) {
                var good_id = edit_args[0];
                var good_name = edit_args[1]
                var quantity = edit_args[2]
                var price = edit_args[3]
                var username = edit_args[4]
                var address = edit_args[5]
                var date = edit_args[6]
                var remark = edit_args[7]
                $.post('/edit_order/', {
                    'id': id,
                    'good_id': good_id,
                    'good_name': good_name,
                    'quantity': quantity,
                    'price': price,
                    'username' : username,
                    'address' : address,
                    'date' : date,
                    'remark' : remark
                }, function (data) {
                    if (data) {
                        alert('修改成功')
                        top.location.reload()
                    }
                });
            } else {
                alert('您输入的内容格式不对，或者缺少必须内容')
            }
        } else {
            alert('你没有输入任何内容')
        }
    }
}
function confirm_order(id) {
    $.post(
			'/confirm_order/',{
				"id" : id
				},
			function (data){
				if(data) {
                    alert('订单已确认')
                    window.location.reload()
                }
			});
}

function trans_order(id) {
    $.post(
			'/trans_order/',{
				"id" : id
				},
			function (data){
				if(data) {
                    alert('订单已发货')
                    window.location.reload()
                }
			});
}