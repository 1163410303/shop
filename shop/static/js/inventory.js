	$(document).ready(function(){
	 $(".tabs").slide({ trigger: "click" });

});
function delete_good(id){
			$.post(
			'/delete_good/',{
				"id" : id
				},
			function (data){
				if(data) {
                    alert('删除成功')
                    top.location.reload()
                }
			});
}
function edit_good(id) {
	var text = prompt("请输入更改后的数据", "商品名称+商品数量+商品描述+商品分类+批发价+零售价"); //将输入的内容赋给变量
	if (text == "商品名称+商品数量+商品描述+商品分类+批发价+零售价") {
		alert('您没有做出任何更改')
    }
	else {
        var edit_args = text.split('+');
        if (text)//如果返回的有内容
        {
            if (edit_args.length == 6) {
                var name = edit_args[0];
                var quantity = edit_args[1]
                var content = edit_args[2]
                var type_name = edit_args[3]
                var trade_price = edit_args[4]
                var retail_price = edit_args[5]
                $.post('/edit_good/', {
                    'id': id,
                    'name': name,
                    'quantity':quantity,
                    'content': content,
                    'type_name': type_name,
                    'trade_price': trade_price,
                    'retail_price': retail_price
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