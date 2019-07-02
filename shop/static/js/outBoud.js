	$(document).ready(function(){
	 $(".tabs").slide({ trigger: "click" });

});
function delete_outboud(id){
			$.post(
			'/delete_outboud/',{
				"id" : id
				},
			function (data){
				if(data) {
                    alert('删除成功')
                    top.location.reload()
                }
			});
}
function edit_outboud(id) {
	var text = prompt("请输入更改后的数据", "商品名称+商品分类+出库数量+出库日期+备注"); //将输入的内容赋给变量
	if (text == "商品名称+商品分类+出库数量+出库日期+备注") {
		alert('您没有做出任何更改')
    }
	else {
        var edit_args = text.split('+');
        print()
        if (text)//如果返回的有内容
        {
            if (edit_args.length == 5) {
                var name = edit_args[0];
                var type_name = edit_args[1]
                var quantity = edit_args[2]
                var date = edit_args[3]
                var remark = edit_args[4]
                $.post('/edit_outboud/', {
                    'id': id,
                    'name': name,
                    'type_name': type_name,
                    'quantity': quantity,
                    'date': date,
                    'remark': remark
                }, function (data) {
                    if (data.msg == 'OK') {
                        alert('修改成功')
                        top.location.reload()
                    }else if(data.msg == 'null') {
                        alert('没有该商品')
                        top.location.reload()
                    }else {
                        alert('商品数量不足')
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