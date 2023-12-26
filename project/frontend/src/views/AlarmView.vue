<template>
  <div class="intro">
    <span class="intro-title">异常监测</span>
    <div class="tool-bar">
      <a-select class="setting-button" v-model="form.selectedDevice" @update:value="updateSelectedDevice" style="width: 177px;" placeholder="选择设备">
        <a-select-option
          v-for="device in devices"
            :key="device.value"
            :label="device.text"
            :value="device.value"
        >{{ device.text }}</a-select-option>
      </a-select>
      <a-select class="setting-button" v-model="form.selectedEvent" @update:value="updateSelectedEvent" style="width: 177px;" placeholder="按事件筛选异常数据" :allowClear='true'>
        <a-select-option
          v-for="event in availableEvents"
            :key="event[0]"
            :label="event[0]"
            :value="event[0]"
        ></a-select-option>
      </a-select>
      <a-button class="setting-button" type="primary" @click="setThresholds">更改阈值</a-button>
      <a-button class="setting-button" style="margin-right: 60px;" type="primary" @click="setAlarm">设置提醒方式</a-button>
    </div>
  </div>
  <div class="main">
    <div style="text-align: left;">
      <a-modal v-model:visible="thresholds" title="更改阈值" @ok="setThresholdsOK" @cancel="setThresholdsCancel">
        <div class="tool-item">
          <span class="prompt">x : </span>
          <a-slider style="flex: 1;" v-model:value="threshold_x" :min="0" :max="36" :step="0.1" />
          <a-input-number v-model:value="threshold_x" :min="0" :max="36" />
        </div>
        <div class="tool-item">
          <span class="prompt">y : </span>
          <a-slider style="flex: 1;" v-model:value="threshold_y" :min="0" :max="36" :step="0.1" />
          <a-input-number v-model:value="threshold_y" :min="0" :max="36" />
        </div>
        <div class="tool-item">
          <span class="prompt">z : </span>
          <a-slider style="flex: 1;" v-model:value="threshold_z" :min="0" :max="36" :step="0.1" />
          <a-input-number v-model:value="threshold_z" :min="0" :max="36" />
        </div>
      </a-modal>
      <a-modal v-model:visible="alarm" title="设置提醒方式" @ok="setAlarmOK" @cancel="setAlarmCancel">
        <div class="tool-item">
          <a-checkbox v-model:checked="isReceivingEmail">邮箱</a-checkbox>
          <a-input style="width: 80%;" v-model:value="email" placeholder="请输入邮箱" />
        </div>
        <div class="policy">
          提供邮箱即表示同意<a href="/#/PrivacyPolicy" target="_blank">隐私政策</a>。
        </div>
      </a-modal>
    </div>
    <div class="data-table">
      <div class="info-bar">
        <!-- <a-radio-group class="option-button" v-model:value="currSelect" button-style="solid">
          <a-radio-button value="chart" :disabled="noSelectedDevice" @click="selectChart">图表显示</a-radio-button>
          <a-radio-button value="list" :disabled="noSelectedDevice" @click="selectList">列表显示</a-radio-button>
        </a-radio-group> -->
        <!-- <p class="time-period" v-if="form.selectedEvent" v-text="eventInfo"></p> -->
        <a-button class="download-button" button-style="solid" :disabled="noData" @click="downloadData">下载csv文件</a-button>
      </div>
      <a-table class="table" v-if="noSelectedDevice" :columns="columns"/>
      <div ref="myChart" style="height: 395px;"></div>
      <a-table class="table" :pagination="customPagination" :columns="columns" @change="tableChange" :dataSource="deviceData" v-show="!noSelectedDevice"/>
    </div>
  </div>
</template>
  
<script>
import { ref, onMounted, h } from 'vue';
import { Table, Form, FormItem, Select, SelectOption, DatePicker, Button, Modal, Slider, Input, InputNumber, Checkbox, RadioGroup, RadioButton, message } from 'ant-design-vue';
import * as echarts from 'echarts';
import store from '@/store';
  
export default {
  components: {
    ATable: Table,
    AForm: Form,
    AFormItem: FormItem,
    ASelect: Select,
    ASelectOption: SelectOption,
    ADatePicker: DatePicker,
    AButton: Button,
    AModal: Modal,
    ASlider: Slider,
    AInput: Input,
    AInputNumber: InputNumber,
    ACheckbox: Checkbox,
    ARadioGroup: RadioGroup,
    ARadioButton: RadioButton,
  },
  setup() {
    const devices = ref([]);
    const deviceData = ref([]);
    const noData = ref(true);

    const title = () => '异常数据' +  eventInfo.value;
    const form = ref({
      selectedDevice: [],
      selectedEvent: [],
    });
    const noSelectedDevice = ref(true);

    const availableEvents = ref([]);
    const eventInfo = ref("");

    const thresholds = ref(false);
    const alarm = ref(false);
    const threshold_x = ref(0);
    const threshold_y = ref(0);
    const threshold_z = ref(0);

    const email = ref("");
    const isReceivingEmail = ref(false);

    const myChart = ref(null);
    const showChart = ref(true);
    const showList = ref(false);
    const currSelect = ref("chart");

    const displayOptions = [
      { value: 'chart', label: '图表显示' },
      { value: 'list', label: '列表显示' }
    ]

    const selectChart = () => {
      showChart.value = true;
      showList.value = false;
      currSelect.value = "chart";
    }

    const selectList = () => {
      if (noSelectedDevice.value) {
        message.error('请先选择设备');
      } else {
        console.log('not seleced? ', noSelectedDevice.value);
        showChart.value = false;
        showList.value = true;
        currSelect.value = "list";
      }
    }

    const updateSelectedDevice = (value) => {
      noSelectedDevice.value = false;
      form.value.selectedDevice = value;
      console.log('form.value.selectedDevice', form.value.selectedDevice);
      getAnomaly();
    };
    
    const updateSelectedEvent = async (value) => {
      form.value.selectedEvent = value;
      await getEventInfo();
      console.log('form.value.selectedEvent', form.value.selectedEvent);
      if (!noSelectedDevice.value) {
        getAnomaly();
      }
    };

    const customPagination = ref({
      total: 0,
      current: 1,
      defaultPageSize: 10,
      showTotal: total => `共 ${total} 条数据`,
      showSizeChanger: true,
      pageSizeOptions: ['5', '10'],
      onShowSizeChange: (current, pageSize) => this.pageSize = pageSize
    });

    const tableChange = (pagination, filters, sorter) => {
      customPagination.value = pagination;
    };

    const columns = [
      {
        title: '序号',
        dataIndex: 'index',
        key: 'index',
        customRender: (text, record, index) => `${(customPagination.value.current - 1) * customPagination.value.defaultPageSize + text.renderIndex + 1}`,
      },
      {
        title: '时间段',
        dataIndex: 'time',
        key: 'time',
      },
      {
        title: 'x',
        dataIndex: 'x',
        key: 'x',
        sorter: (a, b) => (a.x > 0 ? a.x : -a.x) - (b.x > 0 ? b.x : -b.x),
        customRender: (text, record) => {
          // 超过阈值的数据标红
          if (Math.abs(text.value) > threshold_x.value) {
            return h('span', { style: { color: 'red' } }, text.value);
          } else {
            return h('span', { style: { color: 'black' } }, text.value);
          }
        }
      },
      {
        title: 'y',
        dataIndex: 'y',
        key: 'y',
        sorter: (a, b) => (a.y > 0 ? a.y : -a.y) - (b.y > 0 ? b.y : -b.y),
        customRender: (text, record) => {
          // 超过阈值的数据标红
          if (Math.abs(text.value) > threshold_y.value) {
            return h('span', { style: { color: 'red' } }, text.value);
          } else {
            return h('span', { style: { color: 'black' } }, text.value);
          }
        }
      },
      {
        title: 'z',
        dataIndex: 'z',
        key: 'z',
        sorter: (a, b) => (a.z > 0 ? a.z : -a.z) - (b.z > 0 ? b.z : -b.z),
        customRender: (text, record) => {
          // 超过阈值的数据标红
          if (Math.abs(text.value) > threshold_z.value) {
            return h('span', { style: { color: 'red' } }, text.value);
          } else {
            return h('span', { style: { color: 'black' } }, text.value);
          }
        }
      },
    ];

    const getAvailableEvents = async () => {
      const response = await fetch('http://127.0.0.1:5000/api/event_names');
      availableEvents.value = await response.json();
    };

    const getEventInfo = async() => {
      if (!form.value.selectedEvent) {
        eventInfo.value = "";
        return;
      }
      const eventInfoResponse = await fetch('http://127.0.0.1:5000/api/get_event_info', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          event_name: form.value.selectedEvent
        }),
      });
      const info = await eventInfoResponse.json();
      const eventStartDate = new Date(info[0][0]);
      const formattedStarDate = eventStartDate.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
      const eventEndDate = new Date(info[0][1]);
      const formattedEndDate = eventEndDate.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
      eventInfo.value = ' - ' + formattedStarDate + ' - ' + formattedEndDate;
    }

    const getDevices = async () => {
      const response = await fetch(`http://127.0.0.1:5000/api/all`);
      const data = await response.json();
      devices.value = data.map(item => {
        return {
          text: item.join(' '),
          value: item[0]
        };
      });
      console.log('devices', devices.value);
    };

    const createChart = (data) => {
      if (myChart.value) {
        try {
          const chart = echarts.init(myChart.value);

          const option = {
            // ECharts configuration goes here
            title: {
              text: '异常数据'  + eventInfo.value,
              x: 'center',
            },
            legend: {
              top: '7%',
              data: ['x', 'y', 'z'],
            },
            tooltip: {
              trigger: 'axis',
              formatter: function (params) {
                return '时间段: ' + data[params[0].dataIndex].time + '<br/><span style="color:red;">● </span>x: <span style="font-weight:bold;">' + data[params[0].dataIndex].x + '</span><br/><span style="color:green;">● </span>y: <span style="font-weight:bold;">' + data[params[0].dataIndex].y + '</span><br/><span style="color:blue;">● </span>z: <span style="font-weight:bold;">' + data[params[0].dataIndex].z + '</span>';
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
            series: [
              {
                name: 'x',
                type: 'scatter',
                data: data.map(function (item) {
                  return item.x;
                }),
                symbolSize: 5,
                itemStyle: {
                  color: 'red'
                },
                markLine: {
                  symbol: 'none',
                  data: [
                    {
                      yAxis: threshold_x.value,
                      label: {
                        show: true,
                        formatter:"x阈值上限"
                      },
                      lineStyle: {
                        type: 'solid',
                        color: 'red',
                        width: 0.5,
                      },
                    },
                    {
                      yAxis: -threshold_x.value,
                      label: {
                        show: true,
                          formatter:"x阈值下限"
                      },
                      lineStyle: {
                        type: 'solid',
                        color: 'red',
                        width: 0.5,
                      },
                    },
                  ],
                },
              },
              {
                name: 'y',
                type: 'scatter',
                data: data.map(function (item) {
                  return item.y;
                }),
                symbolSize: 5,
                itemStyle: {
                  color: 'green'
                },
                markLine: {
                  symbol: 'none',
                  data: [
                    {
                      yAxis: threshold_y.value,
                      label: {
                        show: true,
                        formatter:"y阈值上限"
                      },
                      lineStyle: {
                        type: 'solid',
                        color: 'green',
                        width: 0.5,
                      },
                    },
                    {
                      yAxis: -threshold_y.value,
                      label: {
                        show: true,
                          formatter:"y阈值下限"
                      },
                      lineStyle: {
                        type: 'solid',
                        color: 'green',
                        width: 0.5,
                      },
                    },
                  ],
                },
              },
              {
                name: 'z',
                type: 'scatter',
                data: data.map(function (item) {
                  return item.z;
                }),
                symbolSize: 5,
                itemStyle: {
                  color: 'blue'
                },
                markLine: {
                  symbol: 'none',
                  data: [
                    {
                      yAxis: threshold_z.value,
                      label: {
                        show: true,
                        formatter:"z阈值上限"
                      },
                      lineStyle: {
                        type: 'solid',
                        color: 'blue',
                        width: 0.5,
                      },
                    },
                    {
                      yAxis: -threshold_z.value,
                      label: {
                        show: true,
                          formatter:"z阈值下限"
                      },
                      lineStyle: {
                        type: 'solid',
                        color: 'blue',
                        width: 0.5,
                      },
                    },
                  ],
                },
              },
            ]
          };
          chart.setOption(option,true);
        } catch (error) {
          console.error('Error initializing ECharts:', error);
        }
      } else {
        console.error('Chart is not initialized or is not a valid DOM element');
      }
    };
    
    const getAnomaly = async () => {
      try {
        console.log('form.value.selectedEvent', form.value.selectedEvent);

        const response = await fetch('http://127.0.0.1:5000/api/anomaly', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            'device_id': form.value.selectedDevice ? form.value.selectedDevice : (devices.value[0].value ? devices.value[0].value : ''),
            'event_name': form.value.selectedEvent ? form.value.selectedEvent : '',
          }),
        });

        const fetchedData = await response.json();
        console.log(fetchedData);

        console.log('Received data from the server:', fetchedData);

        if (Array.isArray(fetchedData)) {
          // Update deviceData with the fetched data
          deviceData.value = fetchedData.map(item => {
            const date = new Date(item[0]);
            const formattedDate = date.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
            const dateBeforeTenMinutes = new Date(date.getTime() - 10 * 60 * 1000);
            const formattedDateBeforeTenMinutes = dateBeforeTenMinutes.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
            const timePeriod = formattedDateBeforeTenMinutes + ' - ' + formattedDate;

            return {
              time: timePeriod,
              x: item[1],
              y: item[2],
              z: item[3],
            };
          }).filter(item => {
            return Math.abs(item.x) > threshold_x.value || Math.abs(item.y) > threshold_y.value || Math.abs(item.z) > threshold_z.value;
          });
          console.log(deviceData.value)

          if (deviceData.value.length == 0) {
            noData.value = true;
          } else {
            noData.value = false;
          }

          createChart(deviceData.value);
        } else {
          console.error('Received non-array data from the server:', fetchedData);
          // Handle the error or return a default value
          return [];
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        // Handle the error or return a default value
        return [];
      }
    };

    const getThresholds = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/thresholds`);
        const data = await response.json();
        threshold_x.value = data['x'];
        threshold_y.value = data['y'];
        threshold_z.value = data['z'];
        console.log('Received data from the server:', data);
        console.log('thresholds', threshold_x.value, threshold_y.value, threshold_z.value);
      } catch (error) {
        console.error('Error fetching data:', error);
        // Handle the error or return a default value
        return [];
      }
    };

    const setThresholds = () => {
      thresholds.value = true;
    };

    const setThresholdsOK = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/set_thresholds', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            'x': threshold_x.value,
            'y': threshold_y.value,
            'z': threshold_z.value,
          }),
        });
        if (!noSelectedDevice.value) {
          getAnomaly();
        }
        message.success('设置成功');
      } catch (error) {
        console.error('Error fetching data:', error);
        // Handle the error or return a default value
        message.error('设置失败, 请检查网络连接或联系网站管理员');
        return [];
      }
      thresholds.value = false;
    };

    const setThresholdsCancel = () => {
      thresholds.value = false;
      getThresholds();
    };

    const getEmail = async () => {
      email.value = localStorage.getItem('email');
      isReceivingEmail.value = localStorage.getItem('isReceivingEmail') == 'true';
      console.log('stored email: ', email.value);
    }
        
    const setAlarm = () => {
      alarm.value = true;
    };

    const setAlarmOK = async () => {
      if (email.value == "") {
        message.error('请输入邮箱');
        return;
      }

      if (email.value.indexOf('@') == -1 || email.value.indexOf('.') == -1) {
        message.error('请输入正确的邮箱');
        return;
      }

      try {
        let storedEmail = "";
        let storedIsReceivingEmail = false;
        storedEmail = localStorage.getItem('email');
        storedIsReceivingEmail = localStorage.getItem('isReceivingEmail');
        if (storedEmail == email.value) {
          // no need to delete the old email
          storedEmail = "";
        }
        localStorage.setItem('email', email.value);
        localStorage.setItem('isReceivingEmail', isReceivingEmail.value);

        const response = await fetch('http://127.0.0.1:5000/api/set_email', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            'old_email': storedEmail,
            'email': email.value,
            'is_receiving_email': isReceivingEmail.value,
          }),
        });
        message.success('设置成功');
      } catch (error) {
        console.error('Error fetching data:', error);
        // Handle the error or return a default value
        message.error('设置失败, 请检查网络连接或联系网站管理员');
        return [];
      }
      alarm.value = false;
    };

    const setAlarmCancel = () => {
      alarm.value = false;
      getEmail();
    };

    const downloadData = () => {
      const device = form.value.selectedDevice;

      console.log('device', device);

      // 创建CSV字符串
      let csv = 'time,x,y,z\n' + deviceData.value.map(row => `${row.time},${row.x},${row.y},${row.z}`).join('\n');

      // 创建一个Blob对象
      let blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });

      // 创建一个可下载的URL
      let url = URL.createObjectURL(blob);

      // 创建一个链接元素
      let link = document.createElement('a');
      link.href = url;
      link.download = device + '.csv';

      // 触发下载
      link.click();
    }

    onMounted(() => {
      getDevices();
      getAvailableEvents();
      getThresholds();
      getEmail();
    });

    return {
      devices,
      deviceData,
      noData,
      availableEvents,
      eventInfo,
      form,
      title,
      myChart,
      noSelectedDevice,
      showChart,
      showList,
      currSelect,
      displayOptions,
      columns,
      customPagination,
      thresholds,
      alarm,
      threshold_x,
      threshold_y,
      threshold_z,
      email,
      isReceivingEmail,
      tableChange,
      selectChart,
      selectList,
      updateSelectedDevice,
      updateSelectedEvent,
      getAnomaly,
      getDevices,
      getAvailableEvents,
      getEventInfo,
      getThresholds,
      setThresholds,
      setThresholdsOK,
      setThresholdsCancel,
      setAlarm,
      setAlarmOK,
      setAlarmCancel,
      downloadData,
    };
  },
};
</script>

<style>
.choices {
  size: 20px;
  margin-top: 50px;
}

.data-table {
  margin: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 8px rgba(10, 10, 10, 0.3);
}

.tool-bar {
  display: flex;
  margin-top: 12px;
}

.info-bar {
  position: relative;
  width: 100%;
  height: 50px;
  margin-top: 20px;
  margin-bottom: 20px;
}

.setting-button {
  margin-left: 28px;
}

.option-button {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  margin: 20px;
}

.download-button {
  position: absolute;
  right: 2%;
  margin-top: 25px;
}

.prompt {
  font-size: medium;
  margin-right: 20px;
}

.ant-table-title {
  text-align: left;
  font-size: 16px;
  font-weight: bold;
}

.table {
  margin-left: 20px;
  margin-right: 20px;
}

.policy {
  text-align: center;
  font-size: small;
  margin-top: 10px;
}
</style>
