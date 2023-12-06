<template>
  <el-container class="main">
    <el-aside class="choices" style="width: 350px; padding-right: 0;">
      <div class="choice_form">
        <a-form :form="form" ref="form" :label-col="{span:4}" :label-align="center" :wrapper-col="{span:16}" :wrapper-align="center">
          <a-form-item label="楼宇" >
            <a-select  class="second-col" v-model="form.selectedBuilding" @update:value="updateSelectedBuilding" placeholder="请选择楼宇" @change="getDevices" style="width: 177px;">
              <a-select-option
                v-for="building in buildings"
                :key="building[0]"
                :label="building[0]"
                :value="building[0]"
              ></a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="设备" >
            <a-select v-model="form.selectedDevice" @update:value="updateSelectedDevice"  placeholder="请选择设备" style="width: 177px;">
              <a-select-option
                v-for="device in devices"
                :key="device[0]"
                :label="device[0]"
                :value="device[0]"
              ></a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="起始" >
            <a-date-picker
              v-model="form.startDate"
              @update:value="StartDime"
              show-time
              format="YYYY-MM-DD HH"
              placeholder="选择起始日期"
              :disabled-date="disabledDate"
            ></a-date-picker>
          </a-form-item>
          <a-form-item label="结束" >
            <a-date-picker
              v-model="form.endDate"
              @update:value="EndTime"
              show-time
              format="YYYY-MM-DD HH"
              placeholder="选择结束日期"
              :disabled-date="disabledDate"
            ></a-date-picker>
          </a-form-item>
        </a-form>
        <a-button class="chaxunbutton" type="primary" @click="getData" >查询数据</a-button>

      </div>
    </el-aside>
    <el-container class="back_canvas">
      <el-header>
        <div class="text_tile">
          <span>振动折线图</span>
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
</template>


<script>
import { ref, onMounted } from 'vue';
import { Form, FormItem, Select, SelectOption, DatePicker, Button, Modal } from 'ant-design-vue';
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
  },
  setup() {
    const form = ref({
      selectedBuilding: [],
      selectedDevice: [],
      startDate: null,
      endDate: null,
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
      console.log(form.value.selectedBuilding);

      const params = new URLSearchParams();
      params.append('building', encodeURIComponent(form.value.selectedBuilding));
      console.log(params.toString());

      const response = await fetch(`http://127.0.0.1:5000/api/devices?${params.toString()}`);
      const data = await response.json();
      devices.value = data;
      console.log(devices);
    };


    const updateSelectedBuilding = (value) => {
      console.log("lalalal");
      console.log(value);
      form.value.selectedBuilding = value;
      console.log( form.value.selectedBuilding)
    };

    const updateSelectedDevice = (value) => {
      console.log("lalalal");
      console.log(value);
      form.value.selectedDevice= value;
      console.log( form.value.selectedDevice)
    };
    const StartDime = (value) => {
      console.log("hahalal");
      console.log(value);
      form.value.startDate= value;
      console.log( form.value.startDate)
    };
    const EndTime = (value) => {
      console.log("hahalal");
      console.log(value);
      form.value.endDate= value;
      console.log( form.value.endDate)
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

      const startTime = form.value.startDate;
      const endTime = form.value.endDate;
      const timeInterval = endTime.diff(startTime, 'hour'); // 这里可以根据需要调整时间间隔的单位


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
           series: Object.keys(data[0]).map((key) => {
          return {
            name: linename[key],
            type: 'line',
            data: data.map((item) => item[key]),

          };
        })
      };

      chart.setOption(option);
    } catch (error) {
      console.error('Error initializing ECharts:', error);
    }
  } else {
    console.error('lineChart is not initialized or is not a valid DOM element');
  }
};
const loading = ref(false);
const queryError = ref(false);

const getData = async () => {
   loading.value = true;
   queryError.value =false; // 重置查询失败标志
  try {
    const response = await fetch('http://127.0.0.1:5000/api/device_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        device_id: form.value.selectedDevice,
       start_date: form.value.startDate ? form.value.startDate.format('YYYY-MM-DD HH') : null,
        end_date: form.value.endDate ? form.value.endDate.format('YYYY-MM-DD HH') : null,
      }),
    });
    console.log(form.value.selectedDevice);

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



    onMounted(() => {
      getBuildings();
      getAvailableDates();

    });

    return {
      loading,
      form,
      buildings,
      devices,
      deviceData,
      lineChart,
      queryError ,
      disabledDate,
      getData,
      getDevices,
      updateSelectedBuilding,
      getBuildings,
      updateSelectedDevice,
      StartDime,
      EndTime
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
}
.choice_form{
  width:280px;
  margin-left: 15px;
  margin-top:20px;
}
.chaxunbutton{
  margin-top: 40px;
  width:150px;
  height: 50px;
  font-size: 20px;
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

  background-color: white;
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
</style>
