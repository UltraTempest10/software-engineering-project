<!-- DataView.vue: 数据可视化页面 -->

<template>
  <el-container class="main">
    <el-aside class="choices" style="width: 350px; padding-right: 0;">
      <div class="choice_form">
        <a-form :form="form_data" ref="form" :label-col="{span:4}" :label-align="center" :wrapper-col="{span:16}" :wrapper-align="center">
          <a-form-item label="楼宇" >
            <a-select  class="second-col" v-model="form_data.selectedBuilding" @update:value="updateSelectedBuilding" placeholder="请选择楼宇" @change="getDevices" style="width: 177px;">
              <a-select-option
                v-for="building in buildings"
                :key="building[0]"
                :label="building[0]"
                :value="building[0]"
              ></a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="设备" >
            <a-select v-model="form_data.selectedDevice" @update:value="updateSelectedDevice"  placeholder="请选择设备" style="width: 177px;">
              <a-select-option
                v-for="device in devices"
                :key="device[0]"
                :label="device[0]"
                :value="device[0]"
              ></a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="方式">
            <a-select v-model="form_data.querymode"  @update:value="updateSelectedmode" placeholder="请选择查询方式"  style="width: 177px;">
              <a-select-option value="time">按时间查询</a-select-option>
              <a-select-option value="event">按事件查询</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item  v-if="form_data.querymode =='time'"  label="起始" >
            <a-date-picker
              v-model="form_data.startDate"
              @update:value="StartDime"
              show-time
              format="YYYY-MM-DD HH"
              placeholder="选择起始日期"
              :disabled-date="disabledDate"
            ></a-date-picker>
          </a-form-item>
          <a-form-item v-if="form_data.querymode =='time'" label="结束" >
            <a-date-picker
              v-model="form_data.endDate"
              @update:value="EndTime"
              show-time
              format="YYYY-MM-DD HH"
              placeholder="选择结束日期"
              :disabled-date="disabledDate"
            ></a-date-picker>
          </a-form-item>
          <a-form-item label="名称" v-if="form_data.querymode =='event'" placeholder="请选择事件名称">
            <a-select v-model="form_data.selectedEvent" @update:value="updateSelectedEvent"  @change="get_event_info" style="width: 177px;">
              <a-select-option
                v-for="event in availableevents"
                :key="event[0]"
                :label="event[0]"
                :value="event[0]"
              ></a-select-option>
            </a-select>
          </a-form-item>
          <p style="text-align: left;" v-if="form_data.querymode =='event'" v-text="form_data.eventinfo" @update:value="get_event_info"> </p>
        </a-form>
        <a-button class="chaxunbutton" type="primary" @click="getData" >查询数据</a-button>

        <div class="gaiyuzhipart">
          <a-form-item label="上限">
            <a-input-number v-model="form_data.upperLimit" :step="0.01" @update:value="updateuplimits" style="width: 137px;"></a-input-number>
          </a-form-item>
          <a-form-item label="下限">
            <a-input-number v-model="form_data.lowerLimit" :step="0.01" @update:value="updatelowlimits" style="width: 137px;"></a-input-number>
          </a-form-item>
          <a-button class="chaxunbutton" type="primary" @click="changelimit" >应用</a-button>
        </div>
      </div>

      <div class="add_new_event_part">
        <a-form :form="eventForm" ref="eventFormRef" :label-col="{span: 4}" :label-align="center" :wrapper-col="{span: 16}" :wrapper-align="center">
          <a-form-item label="名称">
            <a-input v-model="eventData.eventName" @update:value="newEventname" placeholder="请输入事件名称" style="width: 177px;"></a-input>
          </a-form-item>
          <a-form-item label="起始">
            <a-date-picker
              v-model="eventData.startDate"
              @update:value="newEventstarttime"
              show-time
              format="YYYY-MM-DD HH"
              placeholder="选择起始日期"
              :disabled-date="disabledDate"
            ></a-date-picker>
          </a-form-item>
          <a-form-item label="结束">
            <a-date-picker
              v-model="eventData.endDate"
              @update:value="newEventendtime"
              show-time
              format="YYYY-MM-DD HH"
              placeholder="选择结束日期"
              :disabled-date="disabledDate"
            ></a-date-picker>
          </a-form-item>
        </a-form>
        <a-button type="primary" @click="addImportantEvent" class="addbutton">添加事件</a-button>
      </div>
    </el-aside>
    <el-container class="back_canvas">
      <el-header>
        <div class="text_tile">
          <span style="font-weight: bold;">振动折线图</span>
        </div>
      </el-header>
      <el-main>
        <div ref="lineChart" class="chart_data" style="height: 400px;"></div>
      </el-main>
    </el-container>
  </el-container>
  <a-modal v-model:visible="loading" title="查询中" :footer="null" closable>
    <p>正在查询，请稍候...</p>
  </a-modal>
  <a-modal v-model:visible="queryError" title="查询失败" :footer="null" closable>
    <p>查询失败，请检查查询条件。</p>
  </a-modal>
   <a-modal v-model:visible="addsuccess" title="添加成功" :footer="null" closable>
    <p>您已成功添加事件</p>
  </a-modal>

</template>


<script>
import { ref, onMounted,computed,reactive } from 'vue';
import { Form, FormItem, Select, SelectOption, DatePicker, Button, Modal,Input,InputNumber, message } from 'ant-design-vue';
import { Line } from 'vue-chartjs';
import * as echarts from 'echarts'
import dayjs from 'dayjs';

export default {
  extends: Line,
  components: {
    AForm: Form,
    AFormItem: FormItem,
    ASelect: Select,
    ASelectOption: SelectOption,
    ADatePicker: DatePicker,
    AButton: Button,
    'a-modal': Modal,
    AInput:Input,
    AInputNumber:InputNumber
  },
  setup() {
    const form_data = ref({
      selectedBuilding: [],
      selectedDevice: [],
      selectedEvent:[],
      startDate: null,
      endDate: null,
      querymode:[],
      isevent:[],
      upperLimit:0.1,
      lowerLimit:-0.1,
      eventinfo:""
    });

    const buildings = ref([]);
    const devices = ref([]);
    const deviceData = ref([]);


    const lineChart = ref(null); // 使用 ref 来引用图表实例

    const getBuildings = async () => {
      const response = await fetch('http://127.0.0.1:5000/api/buildings');
      const data = await response.json();
      console.log('Buildings Data:', data);
      buildings.value = data;
    };

    const getDevices = async () => {
      console.log("111");
      console.log(form_data.value.selectedBuilding);

      const params = new URLSearchParams();
      params.append('building', encodeURIComponent(form_data.value.selectedBuilding));
      console.log(params.toString());

      const response = await fetch(`http://127.0.0.1:5000/api/devices?${params.toString()}`);
      const data = await response.json();
      devices.value = data;
      console.log(devices);
    };

    const availableevents = ref([]);

    const getAvailableevents = async () => {
      const response = await fetch('http://127.0.0.1:5000/api/event_names');
      availableevents.value = await response.json();
    };


    const updateSelectedBuilding = (value) => {
      console.log("lalalal");
      console.log(value);
      form_data.value.selectedBuilding = value;
      console.log( form_data.value.selectedBuilding)
    };

    const updateSelectedDevice = (value) => {
      console.log("lalalal");
      console.log(value);
      form_data.value.selectedDevice= value;
      console.log( form_data.value.selectedDevice)
    };

    const updateuplimits=(value)=>{
      form_data.value.upperLimit= value;
    }

    const updatelowlimits=(value)=>{
      form_data.value.lowerLimit= value;
    }

    const updateSelectedEvent = (value) => {
      console.log("lalalal");
      console.log(value);
      form_data.value.selectedEvent= value;
      console.log( form_data.value.selectedDevice)
    };

    const updateSelectedmode = (value) => {
      console.log("选方式");
      console.log(value);
      form_data.value.querymode = value;

      console.log( form_data.value.querymode)
      console.log(form_data.value.querymode=='event')

    };

    const StartDime = (value) => {
      console.log("hahalal");
      console.log(value);
      form_data.value.startDate= value;
      console.log( form_data.value.startDate)
    };

    const EndTime = (value) => {
      console.log("hahalal");
      console.log(value);
      form_data.value.endDate= value;
      console.log( form_data.value.endDate)
    };


    const disabledDate = (time) => {
      // Convert available dates to the format used by the date picker
      const availableDateStrings = availableDates.value.map(date => {
        const formattedDate = new Date(date);
        return `${formattedDate.getFullYear()}-${String(formattedDate.getMonth() + 1).padStart(2, '0')}-${String(formattedDate.getDate()).padStart(2, '0')} ${String(formattedDate.getHours()).padStart(2, '0')}:00:00`;
      });

      // Convert the current time to the format used by the date picker
      const currentTimeString = time.format('YYYY-MM-DD HH:00:00');

      // Check if the current time is in the array of available dates
      return !availableDateStrings.includes(currentTimeString);
    };



    const availableDates = ref([]);

    const getAvailableDates = async () => {
      const response = await fetch('http://127.0.0.1:5000/api/available_dates');
      availableDates.value = await response.json();
      console.log(availableDates.value)
    };

    const linename=['delt_x','delt_y','delt_z'];
    const createChart = (data) => {
      if (lineChart.value) {
        try {
          const chart = echarts.init(lineChart.value);

          const startTime = form_data.value.startDate;
          const endTime = form_data.value.endDate;

          const option = {
            // ECharts 图表配置，根据需要设置
            legend: {
              data: ['delt_x', 'delt_y', 'delt_z'], // 图例数据
            },
            tooltip: {
              trigger: 'axis', // 悬停时触发 tooltip
              axisPointer: {
                type: 'cross', // 十字准星指示器
              },
            },

            xAxis: {
              type: 'category',
              data: Array.from({ length: data.length }, (_, i) => i + 1),
            },
            yAxis: {

              name:'单位(gal)',
              type: 'value',

            },

            dataZoom: [
              {
                type: 'inside',
                start: 0,
                end: 100,
              },
              {
                type: 'inside',
                orient: 'vertical',
                start: 0,
                end: 100,
              },
              {
                start: 0,
                end: 100,
                handleIcon:
                  'M10.7,11.7H9.3V10.3h1.3V11.7z M10.7,8.3H9.3V7h1.3V8.3z M10.7,5H9.3V3.7h1.3V5z M10.7,14H9.3v1.3h1.3V14z M14,11.7h-1.3V10.3H14V11.7z M14,8.3h-1.3V7H14V8.3z M14,5h-1.3V3.7H14V5z M14,14h-1.3v1.3H14V14z',
                handleSize: '80%',
                handleStyle: {
                  color: '#fff',
                  shadowBlur: 3,
                  shadowColor: 'rgba(0, 0, 0, 0.6)',
                  shadowOffsetX: 2,
                  shadowOffsetY: 2,
                },
              }
            ],

            series: Object.keys(data[0]).map((key) => {
              return {
                name: linename[key],
                type: 'line',
                data: data.map((item) => item[key]),
                markLine: {
                  symbol: 'none',
                  data: [
                    {
                      yAxis: form_data.value.lowerLimit, // 自定义下限值
                      // name: '最小值', // 基准线名称
                      label: { // 不显示基准线名称
                        show: true,
                        formatter:"下限"
                      },
                      lineStyle: {
                        type: 'solid', // 基准线样式为虚线
                        color: '#b17063',
                        width:2,
                      },
                    },
                    {
                      yAxis: form_data.value.upperLimit, // 上限值
                      // name: '最大值',
                      label: {
                        show: true,
                        formatter:"上限"
                      },
                      lineStyle: {
                        type: 'solid',
                        color: '#b17063',
                        width:2,
                      },
                    },
                  ],
                },
              };
            })
          };

          chart.setOption(option,true);
        } catch (error) {
          console.error('Error initializing ECharts:', error);
        }
      } else {
        console.error('lineChart is not initialized or is not a valid DOM element');
      }
    };


    const loading = ref(false);
    const queryError = ref(false);
    const addsuccess=ref(false);

    const get_event_info=async()=>{
      const eventinfo_response = await fetch('http://127.0.0.1:5000/api/get_event_info', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          event_name:form_data.value.selectedEvent
        }),
      });

      const eventinfo=await eventinfo_response.json();

      console.log(eventinfo);
      console.log(eventinfo[0][0]);

      const eventStartDate = new Date(eventinfo[0][0]);
      const formattedStarDate = eventStartDate.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
      const eventEndDate = new Date(eventinfo[0][1]);
      const formattedEndDate = eventEndDate.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
      form_data.value.eventinfo=formattedStarDate+" - "+formattedEndDate

      console.log("我被执行了");

    }


    const getData = async () => {
      loading.value = true;
      queryError.value =false; // 重置查询失败标志
      try {
        if (form_data.value.querymode=="time") {
          const response = await fetch('http://127.0.0.1:5000/api/device_data', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              device_id: form_data.value.selectedDevice,
              start_date: form_data.value.startDate ? form_data.value.startDate.format('YYYY-MM-DD HH') : null,
              end_date: form_data.value.endDate ? form_data.value.endDate.format('YYYY-MM-DD HH') : null,
            }),
          });

          console.log(form_data.value.selectedDevice);

          const fetchedData = await response.json();

          console.log(fetchedData);
          console.log('Received data from the server:', fetchedData);

          if (Array.isArray(fetchedData)) {
            // Update deviceData with the fetched data
            if (fetchedData.length === 0) {
              console.error('Received an empty array from the server.');
              // 设置查询失败标志
              queryError.value = true;
              // Handle the error or return a default value
              return [];
            }

            deviceData.value = fetchedData;
            console.log("arrivethere")

            createChart(fetchedData);
          } else {
            console.error('Received non-array data from the server:', fetchedData);
            // Handle the error or return a default value
            deviceData.value = [];
            queryError.value = true;
            return [];
          }
        }

        else if (form_data.value.querymode=="event"){
          const response = await fetch('http://127.0.0.1:5000/api/device_data_byevent', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              device_id:form_data.value.selectedDevice,
              event_name:form_data.value.selectedEvent
            }),
          });

          console.log(form_data.value.selectedDevice);

          const fetchedData = await response.json();

          console.log(fetchedData);
          console.log('Received data from the server:', fetchedData);

          if (Array.isArray(fetchedData)) {
            // Update deviceData with the fetched data
            if (fetchedData.length === 0) {
              console.error('Received an empty array from the server.');
              // 设置查询失败标志
              queryError.value = true;
              // Handle the error or return a default value
              return [];
            }

            deviceData.value = fetchedData;
            console.log("arrivethere")

            createChart(fetchedData);
          } else {
            console.error('Received non-array data from the server:', fetchedData);
            // Handle the error or return a default value
            deviceData.value = [];
            queryError.value = true;
            return [];
          }
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        // Handle the error or return a default value
        deviceData.value = [];
        queryError.value = true;
        return [];
      }
      finally {
        loading.value = false; // 查询结束，设置为 false
      }
    };

    const eventData = reactive({
      eventName: '',
      startDate: null,
      endDate: null,
    });

    const changelimit=()=>{
      console.log("arrivethere")
      if (form_data.value.upperLimit < 0) {
        console.log("wrong limit")
        message.error('上限值不能小于0');
      } else if (form_data.value.lowerLimit > 0) {
        message.error('下限值不能大于0');
      } else {
        createChart(deviceData.value);
      }
    };

    const newEventname= (value) => {
      console.log("选方式");
      console.log(value);
      eventData.eventName = value;
    };

    const newEventstarttime= (value) => {
      eventData.startDate = value;
    };

    const newEventendtime= (value) => {
      console.log("选方式");
      console.log(value);

      eventData.endDate = value;
    };

    const addImportantEvent = async () => {
      addsuccess.value=false;
      try {
        const response = await fetch('http://127.0.0.1:5000/api/add_event', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            eventName: eventData.eventName,
            startDate: eventData.startDate ? eventData.startDate.format('YYYY-MM-DD HH') : null,
            endDate: eventData.endDate ? eventData.endDate.format('YYYY-MM-DD HH') : null,
          }),
        });
        console.log("dayin");
        console.log(eventData.eventName);
        const result = await response.json();

        if (result.success) {
          console.log('Event added successfully!');
          addsuccess.value=true;
          // Optionally, you can update the list of available events after adding a new event
          getAvailableevents();
        } else {
          console.error('Failed to add event:', result.error);
        }
      } catch (error) {
        console.error('Error adding event:', error);
      }
    };

  
    onMounted(() => {
      getBuildings();
      getAvailableDates();
      getAvailableevents();
    });


    return {
      loading,
      form_data,
      buildings,
      devices,
      deviceData,
      lineChart,
      queryError ,
      addsuccess,
      availableevents,
      disabledDate,
      getData,
      getAvailableevents,
      getDevices,
      updateSelectedBuilding,
      updateSelectedEvent,
      getBuildings,
      updateSelectedDevice,
      StartDime,
      EndTime,
      updateSelectedmode,
      addImportantEvent,
      eventData,
      newEventname,
      newEventstarttime,
      newEventendtime,
      updateuplimits,
      updatelowlimits,
      changelimit,
      get_event_info

    };
  },
};
</script>


<style>
.choices {
  border-radius: 10px;
  box-shadow: 0px 0px 8px rgba(10, 10, 10, 0.3);
  /* position: absolute; */
  background-color: white;
  size: 30px;
  margin-top: 30px;
  /* margin-left: 40px; */
  height: 760px;
  padding-top: 20px;
  background-color: rgb(255, 255, 230);
}

.choice_form{
  width:280px;
  margin-left: 15px;
  margin-top:20px;
}

.chaxunbutton{
  /* margin-top: 10px; */
  width:120px;
  height: 40px;
  font-size: 18px;
  margin-left: -40px;
}

.addbutton{
  /* margin-top: 10px; */
  width:120px;
  height: 40px;
  font-size: 18px;
  margin-left: -40px;
}

.genggaiyuzhi{
  /* background-color: indianred; */
  margin-left: -40px;
}

.chart_data{
  margin-top:100px ;
  height:1000px;
  width:1300px;
  font-size:30px;
}

.back_canvas{
  border-radius: 10px;
  box-shadow: 0px 0px 8px rgba(10, 10, 10, 0.3);
  /* position: absolute; */

  background-color: rgb(255, 253, 230);
  margin-top: 50px;
  margin-left: 50px;
  border-radius: 10px;
  height:760px;
  margin-right: 20px;
}

.label{
   background-color: black;
}

.a-form-item-label{
  font-size:2px;
}

.text_tile{
  margin-top: 30px;
  font-size:40px;
  letter-spacing: 10px;
}

.container{
  border-radius: 10px;
  box-shadow:inset 0 0 10px #aaaaaa;
  display: flex;
}

.add_new_event_part{
  width:280px;
  margin-left: 15px;
  margin-top: 30px;
}

.gaiyuzhipart{
  width: 280px;
  margin-top: 30px;
}

/* .main{
  background-color: #eeeeee;
} */
</style>
