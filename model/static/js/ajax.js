//原生AJAX函数

function $(name)
{
	return document.getElementById(name);
}

function createAjax()
{
	var XHR = null;

	if(window.XMLHttpRequest)
	{
		XHR = new XMLHttpRequest();
	}
	else
	{
		document.write("Sorry， 只支持非IE内核！！！");
	}

	return XHR;
}

function ajax(id)
{
	XHR = createAjax();

	if(XHR)
	{
                //id = 'http://192.168.132.61:8000/ajaxtest/';
		whiteid = 'white'+id;
		days = $(whiteid).value;
                url = 'http://127.0.0.1:8888/api/listing/'+id+'/'+days+'/';
		//XHR.setRequestHeader("X-Requested-With", "XMLHttpRequest");
		XHR.open("GET",url);

		XHR.onreadystatechange = function()
		{
			if(XHR.readyState == 4 && XHR.status == 200)
			{
                                //document.write(XHR.responseText);
				alert(id+' Modify Success!\n  Now Value is '+days+'.')

				XHR = null;
			}
		}
		XHR.send();
	}
}
