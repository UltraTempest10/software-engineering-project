//tab-nav组件
Vue.component("tab-nav",{
    template:`
    <div class="tab-nav">
        <ul class="tab-list">
	    <li style="font-size:24px;font-weight: bold;color: red;">幕墙前端</li>
            <li v-bind:class="{active:tabli==0}" @click="linkPage(0)">首页</li>
            <li v-bind:class="{active:tabli==1}" @click="linkPage(1)">图片轮播</li>
            <li v-bind:class="{active:tabli==2}" @click="linkPage(2)">数据展示</li>
            <li v-bind:class="{active:tabli==3}" @click="linkPage(3)">警报器系统</li>
	    <li style="font-size:24px;font-weight: bold;color: red;">
<div>
    <input id="mytext" type="text" name="username" placeholder="请输入搜索内容" maxlength="6">
    <button>搜索</button>
  </div>
		</li>
        </ul>
    </div>
    `,
    props:["tabli"],
    data(){
      return{ 
        
      }
    },
    methods:{
      linkPage(pid){
        console.log(pid);
        switch(pid){
          case 1:
            location.href = 'picture.html';
            break;
          case 2:
            location.href = 'dataview.html';
            break;
          case 3:
            location.href = 'other.html';
            break;
          default:
            location.href = 'index.html';
            break;
        }
        
     }

    },
    components:{
    }
  })