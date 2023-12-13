<template>
  <div class="intro">
    
    <span class="intro-title">自动报警</span>
    <div class="tool-bar">
      <a-select class="setting-button" v-model="form.selectedEvent" @update:value="updateSelectedEvent" style="width: 177px;" placeholder="按事件筛选异常数据">
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
    
    <!-- <div class="block-container">
      <Feature
        :image="require('@/assets/img/monitoring.png')"
        title="实时监测"
        description="24小时监测玻璃幕墙加速度数据，不放过任何异常。"
      />
      <Feature
        :image="require('@/assets/img/alarm.png')"
        title="邮件报警"
        description="发现异常后，通过邮件向用户发送警告，以便及时处理风险。"
      />
    </div> -->
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
          <a-checkbox v-model="mail">邮箱</a-checkbox>
        </div>
      </a-modal>
    </div>
    <div class="data-table">
      <a-table :columns="columns" :dataSource="deviceData" :title="title"/>
    </div>
  </div>
</template>
  
<script>
import { ref, onMounted } from 'vue';
import { Table, Form, FormItem, Select, SelectOption, DatePicker, Button, Modal, Slider, InputNumber, Checkbox, message } from 'ant-design-vue';
import Feature from '/src/components/IntroBlock.vue';
  
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
    AInputNumber: InputNumber,
    ACheckbox: Checkbox,
    Feature,
  },
  setup() {
    const devices = ref([]);
    const deviceData = ref([]);
    const title = () => '异常数据';
    const form = ref({
      selectedEvent: [],
    });

    const updateSelectedEvent = (value) => {
      form.value.selectedEvent = value;
      getAnomaly();
    };

    const columns = [
      {
        title: 'ID',
        dataIndex: 'id',
        key: 'id',
        filters: [],
        filterSearch: true,
        onFilter: (value, record) => record.id.indexOf(value) === 0,
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
        sorter: (a, b) => a.x - b.x,
      },
      {
        title: 'y',
        dataIndex: 'y',
        key: 'y',
        sorter: (a, b) => a.y - b.y,
      },
      {
        title: 'z',
        dataIndex: 'z',
        key: 'z',
        sorter: (a, b) => a.z - b.z,
      },
    ];

    const availableEvents = ref([]);

    const getAvailableEvents = async () => {
      const response = await fetch('http://127.0.0.1:5000/api/event_names');
      availableEvents.value = await response.json();
    };

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
      columns[0].filters = devices.value;
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
            'event_name': form.value.selectedEvent ? form.value.selectedEvent : '',
          }),
        });

        const fetchedData = await response.json();
        console.log(fetchedData);

        console.log('Received data from the server:', fetchedData);

        if (Array.isArray(fetchedData)) {
          // Update deviceData with the fetched data
          deviceData.value = fetchedData.map(item => {
            const date = new Date(item[1]);
            const formattedDate = date.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
            const dateBeforeTenMinutes = new Date(date.getTime() - 10 * 60 * 1000);
            const formattedDateBeforeTenMinutes = dateBeforeTenMinutes.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
            const timePeriod = formattedDateBeforeTenMinutes + ' - ' + formattedDate;

            return {
              id: item[0],
              time: timePeriod,
              x: item[2],
              y: item[3],
              z: item[4],
            };
          }).filter(item => {
            return Math.abs(item.x) > threshold_x.value || Math.abs(item.y) > threshold_y.value || Math.abs(item.z) > threshold_z.value;
          });
          console.log(deviceData.value)
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

    const thresholds = ref(false);
    const alarm = ref(false);
    const threshold_x = ref(0);
    const threshold_y = ref(0);
    const threshold_z = ref(0);

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
        getAnomaly();
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

    const mail = ref(false);

    const setAlarm = () => {
      alarm.value = true;
    };

    const setAlarmOK = async () => {
      try {
        
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
    };

    onMounted(() => {
      getAnomaly();
      getDevices();
      getAvailableEvents();
      getThresholds();
    });

    return {
      devices,
      deviceData,
      availableEvents,
      form,
      title,
      columns,
      thresholds,
      alarm,
      threshold_x,
      threshold_y,
      threshold_z,
      updateSelectedEvent,
      getAnomaly,
      getDevices,
      getAvailableEvents,
      getThresholds,
      setThresholds,
      setThresholdsOK,
      setThresholdsCancel,
      setAlarm,
      setAlarmOK,
      setAlarmCancel,
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

.setting-button {
  margin-left: 28px;
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
</style>
