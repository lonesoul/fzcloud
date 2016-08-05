	function disktubiao(mainid,linenameW,linenameR,xdata,ydataW,ydataR,yUnit){
			//图表
			
			 // 路径配置
        require.config({
            paths: {
                echarts: '/static/js/build/dist'
            }
        });
		   // 使用
        require(
            [
                'echarts',
				'echarts/chart/line',
            ],
          //渲染ECharts图表

			function(ec){
			
				//图表渲染的容器对象
				
				var myChart = ec.init(document.getElementById(mainid));
				myChart.showLoading({text: '正在努力的读取数据中...'});  
				//加载图表
				option = {
			
			
					//数据提示框配置
			
					tooltip: {
						trigger: 'axis', //触发类型，默认数据触发，见下图，可选为：'item' | 'axis' 其实就是是否共享提示框
								formatter: function (params){

									var res=params[0].name;
									for(var i=0,l=params.length;i<l;i++){
										if (yUnit == 'M'){
											res += '<br/>'+params[i].seriesName+':' +(params[i].value/1024/1024).toFixed(2)+'MB/s';
										}else if(yUnit == 'K'){
											res += '<br/>'+params[i].seriesName+':' +(params[i].value/1024).toFixed(2)+'KB/s';
										}else{
											res += '<br/>'+params[i].seriesName+':' +(params[i].value).toFixed(2)+'B/s';
										}
									}
									return res;
									
								},
					},
			
					//图例配置
			
					legend: {

						orient : 'horizontal',  
						data: [
							{
								name:linenameW,
								textStyle:{
									color:'#EF4542',
									
								},
								icon: 'image:///static/images/charts/iconfont-04.png',
							},
							{
								name:linenameR,
								textStyle:{
									color:'#2C9CFF',
									
								},
								icon: 'image:///static/images/charts/iconfont-04.png',
							},
						], //这里需要与series内的每一组数据的name值保持一致
						//x : 'left',
						//y:"bottom",
						backgroundColor:'rgba(0,0,0,0)',
						//borderColor:'red',

						selectedMode:'multiple',
					},

			

					calculable: true,
			        dataZoom : {
                        show : true,
                        //realtime : true,
                        start : 20,
                        end : 80
                    },
					//X轴配置
							
					xAxis : [
						{
							type : 'category',
							position: 'bottom',
							boundaryGap: false,
							axisLine : {    // 轴线
								show: true,
								lineStyle: {
									color: 'green',
									type: 'solid',
									width: 2
								}
							},
							axisLabel : {
								show:true,
								interval: 'auto',    // {number}
								rotate: 0,
								margin: 8,
								formatter: '{value}',
								textStyle: {
									color: '#888',
									fontFamily: 'sans-serif',
									fontSize: 10,
									fontStyle: 'italic',
									fontWeight: 'none',
									align: 'left',
								}
							},
							splitLine : {     //X轴对应竖线
								show:true,
								lineStyle: {
									color: '#ddd',
									type: 'dashed',
									width: 1
								}
							},
							data : function(){
                                var list = [];
                                for (var i=0; i <xdata.length; i++){
                                    list.push(xdata[i]);
                                }
                                return list;
                            }()
							/*[
								'14:17','14:15','3','4','5',6,
								'7','8','9','14:13','14:15','14:17'
							]*/
						 }
					],
			
					//Y轴配置
			
					yAxis : [
						{
							type : 'value',
							position: 'left',
							//min: 0,
							//max: 100,
							splitNumber: 5,
							axisLine : {    // 轴线
								show: false,
								lineStyle: {
									color: 'green',
									type: 'solid',
									width: 2
								}
							},
							splitArea : {
								show: true,
								areaStyle:{
									color:['rgba(246,246,246,0.5)','rgba(255,255,255,0.5)']
								}
							},
							axisLabel : {
								show:true,
								interval: 'auto',    // {number}
								rotate: 0,
								margin: 15,
								//formatter: '{value}',    // Template formatter!
								formatter: function (value){
									if (yUnit == 'M'){
										return (value /1000/1000)+'MB/s';
									}else if (yUnit =='K'){
										return (value /1000)+'KB/s';
									}else{
										return (value)+'B/s';
									}
										
								},
								textStyle: {
									color: '#ddd',
									fontFamily: 'verdana',
									fontSize: 12,
									fontStyle: 'normal',
									fontWeight: 'bold'
								},
							},

						},
					],
			
					//图表Series数据序列配置
			
					series: [
			
						{
			
							name: linenameW,
							
							type: 'line',
							smooth:true,//线条圆润
							symbol: 'image:///static/images/charts/iconfont-04.png',//节点图标symbol: 'image://../asset/ico/',     // 系列级个性化拐点图形
							//symbolSize: 8,//拐点图形大小
							 itemStyle: {
								normal: {
									areaStyle: {
										// 区域图，纵向渐变填充
										color : (function (){
											var zrColor = require('zrender/tool/color');
											return zrColor.getLinearGradient(
												0, 200, 0, 400,
												[[0, 'rgba(249, 176, 174,0.8)'],[0.8, 'rgba(249, 176, 174,0.1)']]
											)
										})()
									},
									lineStyle: {
										width: 2,
										color: (function (){
											var zrColor = require('zrender/tool/color');
											return zrColor.getLinearGradient(
												0, 0, 1000, 0,
												[[0, 'rgba(239, 69, 66,0.8)'],[0.8, 'rgba(239, 69, 66,0.8)']]
											)
										})(),
										shadowColor : 'rgba(0,0,0,0.5)',
										shadowBlur: 10,
										shadowOffsetX: 8,
										shadowOffsetY: 8
									},
									
								},
							 
							 },
							 data: ydataW,
							//data: [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 80.6, 12.2, 32.6, 20.0, 6.4, 3.3]
			
						},
{
			
							name: linenameR,
							
							type: 'line',
							smooth:true,//线条圆润
							symbol: 'image:///static/images/charts/iconfont-04.png',//节点图标symbol: 'image://../asset/ico/',     // 系列级个性化拐点图形
							//symbolSize: 8,//拐点图形大小
							 itemStyle: {
								normal: {
									areaStyle: {
										// 区域图，纵向渐变填充
										color : (function (){
											var zrColor = require('zrender/tool/color');
											return zrColor.getLinearGradient(
												0, 200, 0, 400,
												[[0, 'rgba(162, 173, 214,0.8)'],[0.8, 'rgba(162, 173, 214,0.1)']]
											)
										})()
									},
									lineStyle: {
										width: 2,
										color: (function (){
											var zrColor = require('zrender/tool/color');
											return zrColor.getLinearGradient(
												0, 0, 1000, 0,
												[[0, 'rgba(44, 156, 255,0.8)'],[0.8, 'rgba(44, 156, 255,0.8)']]
											)
										})(),
										shadowColor : 'rgba(0,0,0,0.5)',
										shadowBlur: 10,
										shadowOffsetX: 8,
										shadowOffsetY: 8
									},
									
								},
							 
							 },
							 data: ydataR,
							//data: [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 80.6, 12.2, 32.6, 20.0, 6.4, 3.3]
			
						},			
					]
			
				};
				myChart.setOption(option);
				myChart.hideLoading();  
			}
        );
		//图标结束
	}
	//磁盘图表结束
