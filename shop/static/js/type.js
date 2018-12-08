	$(document).ready(function(){
	 $(".tabs").slide({ trigger: "click" });

});
function delete_type(id){
			$.post(
			'/delete_type/',{
				"id" : id
				},
			function (data){
				if(data) {
                    alert('删除成功')
                    top.location.reload()
                }
			});
}
function edit_type(id) {
	var text = prompt("请输入更改后的数据", "种类名称+种类描述+备注"); //将输入的内容赋给变量
	if (text == "种类名称+种类描述+备注") {
		alert('您没有做出任何更改')
    }
	else {
        var edit_args = text.split('+');
        if (text)//如果返回的有内容
        {
            if (edit_args.length == 3) {
                var type_name = edit_args[0];
                var description = edit_args[1]
                var remark = edit_args[2]
                $.post('/edit_type/', {
                    'id': id,
                    'type_name': type_name,
                    'description': description,
                    'remark': remark
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

