<!-- FramePlayer.vue: 图片播放页面 -->

<template>
  <div class="intro">
    <span class="intro-title">图片播放</span>
    <div class="block-container">
      <Feature
        :image="require('@/assets/img/camera.png')"
        title=""
        description="提供高清晰度的玻璃幕墙动态图片，让用户可以清晰地观察细节。"
      />
      <Feature
        :image="require('@/assets/img/drone.png')"
        title=""
        description="通过无人机进行多个位置的拍摄，仔细检查每一部分的外立面。"
      />
    </div>
  </div>
  <el-container class="main">
  
    <el-aside style="width: 400px">
      <div class="tools">
        <!-- <el-row> -->
          <!-- <el-icon style="font-size: 32px;">
            <Camera />
          </el-icon> -->
        <!-- </el-row> -->
        <label class="tool-item">
          <span>播放速度(每秒帧数):</span>
          <el-input-number v-model="setfps" :min="1" :max="30" controls-position="right"></el-input-number>
        </label>
      </div>
      <div class="tools">
        <!-- <el-row>
          <el-icon style="font-size: 32px;">
            <Picture />
          </el-icon>
        </el-row> -->
        <label class="tool-item">
          <span>位置:</span>
          <el-form-item>
            <el-select style="width: 150px;" v-model="selectedLocation" placeholder="请选择拍摄位置">
              <el-option label="衷和楼10-15楼" value="衷和楼10-15楼" />
              <el-option label="衷和楼16-21楼" value="衷和楼16-21楼" />
            </el-select>
          </el-form-item>
          <el-button type="primary" @click="saveAndRefresh">确定</el-button>
        </label>
      </div>
    </el-aside>

    <el-container>
      <el-main>

        <div class="box">
          <div class="framePlayer"></div>
          <div class="control">
            <i class="fa fa-play"></i>
            <i class="fa fa-pause"></i>
            <i class="fa fa-backward"></i>
            <i class="fa fa-forward"></i>
            <i class="fa fa-refresh"></i>
            <i class="fa fa-download"></i>
            <div class="process_bar">
              <div class="process"></div>
            </div>
          </div>
          <div class="info">
            <div class="coordinates">横坐标：{{ xCoordinate }}</div>
            <div class="coordinates">纵坐标：{{ yCoordinate }}</div>
          </div>          

        </div>

      </el-main>
    </el-container>
  </el-container>
</template>
    

<script>
import { Options, Vue } from 'vue-class-component';
import { ElMessage, ElMessageBox } from 'element-plus';
import { VideoPlay, VideoPause } from '@element-plus/icons-vue'; // @ is an alias to /src
import "@/assets/css/style.css"
import "@/assets/css/font-awesome.min.css"
import vFramePlayer from '@/assets/js/vframeplayer';
import $ from 'jquery'
import { ref, onMounted, watch, reactive } from 'vue';
import Feature from '/src/components/IntroBlock.vue';

export default {
  components: {
    Feature,
  },

  setup() {
    const setfps = ref(8);
    const selectedLocation = ref('衷和楼10-15楼');
    let framePlayer = null;
    const xCoordinate = ref(0);
    const yCoordinate = ref(0);

    var imgArr = [];

    const saveAndRefresh = () => {
      // 保存当前选择的拍摄位置到 localStorage
      localStorage.setItem('selectedLocation', selectedLocation.value);
      // 刷新页面
      location.reload();
    };

    const pushImage = () =>{
      imgArr.length = 0; // 清空之前的图片数组内容
      if(selectedLocation.value==="衷和楼16-21楼"){
        for (var i = 0; i < 89; i++) {
            imgArr.push("https://curtain-wall.oss-cn-shanghai.aliyuncs.com/%E8%A1%B7%E5%92%8C%E6%A5%BC/16-21%E6%A5%BC/" + i + ".jpg?324324324");
        }
      }
      if(selectedLocation.value==="衷和楼10-15楼"){
        for (var i = 0; i < 89; i++) {
            imgArr.push("https://curtain-wall.oss-cn-shanghai.aliyuncs.com/%E8%A1%B7%E5%92%8C%E6%A5%BC/10-15%E6%A5%BC/" + i + ".jpg?324324324");
        }
      }
    };


    onMounted(() => {

      $(document).ready(function () {

        var info = $(".info");
        var process = $(".process");
        var settings = $(".settings");
        

        function loadImages(Parameter) {
          var sources = Parameter.loadArr;	//图片资源
          var loadingPercent = "";
          var count = 0;
          var images = {};
          var imgNum = sources.length;	//图片数量
          for (var src in sources) {
            var path = src;
            images[path] = new Image();
            images[path].onload = function () {
              count++;
              if (count >= imgNum) {
                Parameter.complete(images);
              }
            };
            images[path].onerror = function () {
              count++;
              if (count >= imgNum) {
                Parameter.complete(images);
              }
            };
            images[path].src = sources[path];
          }
        };

        var framePlayer;

        pushImage();

        var dom = document.getElementById("framePlayer");
        console.log(dom);

        loadImages({
          loadArr: imgArr,
          complete: function () {
            framePlayer = new vFramePlayer({
              dom: $(".framePlayer")[0],
              imgArr: imgArr,
              loop: 0,
              yoyo: true,
              useCanvas: true
            });
            framePlayer.goto(framePlayer.get("startFrame"));

            var default_set = function () {
              settings.find(".yoyo").attr("checked", framePlayer.get("yoyo"));
              settings.find(".times").val(framePlayer.get("loop"));
              settings.find(".fps").val(framePlayer.get("fps"));
              settings.find(".start").val(framePlayer.get("startFrame")).attr("max", imgArr.length - 1);
              settings.find(".end").val(framePlayer.get("endFrame")).attr("max", imgArr.length - 1);
              var mode_id = framePlayer.get("useCanvas") ? 0 : 1;
              settings.find(".mode[name='mode']").eq(mode_id).attr('checked', 'true');
            };

            default_set();

            framePlayer.on("update", function (frame, times, asc) {

              info.find(".curFrame").find("span").text(frame);
              info.find(".times").find("span").text(times);
              info.find(".asc").find("span").text(asc);
              info.find(".fps").find("span").text(framePlayer.get("fps"));

              yCoordinate.value = Math.ceil(frame/8);
              if(frame!==0){
                if(yCoordinate.value%2===0){
                  if(frame%16===0){
                    xCoordinate.value=1;
                  }
                  else{
                    xCoordinate.value=9-(frame%8)||8;
                  }
                }              
                else{
                  xCoordinate.value=frame%8||8;
                }

              }   

              var process_total = imgArr.length - 1;
              var a = 100 / process_total;
              process.css({ "width": frame * a + "%" });

            });

            $(".fa-play").on("click", function () {
              var fps = $(".fps").val();
              var start = settings.find(".start").val();
              var end = settings.find(".end").val();
              framePlayer.play(start, end, {
                "fps": setfps.value, "yoyo": false, "useCanvas": true, onComplete: function () {
                  //                      console.log("完成播放");
                }, onUpdate: function (frame, times, asc) {
                  //                      console.log(frame,times,asc);
                }
              });
            });

            $(".fa-pause").on("click", function () {
              framePlayer.pause();
            });

          //上一张
          $(".fa-backward").on("click", function () {
            framePlayer.backward();
          });

          $(".fa-forward").on("click", function () {
            framePlayer.forward();
          });

          $(".fa-refresh").on("click", function () {
            framePlayer.gotoStartFrame();
          });
          
          $(".fa-download").on("click", function () {
            if(selectedLocation.value==="衷和楼10-15楼"){
              var url = "https://curtain-wall.oss-cn-shanghai.aliyuncs.com/raw/" + framePlayer.get("curFrame") + ".jpg?324324324" ;
            }
            else if(selectedLocation.value==="衷和楼16-21楼"){
              var url = "https://curtain-wall.oss-cn-shanghai.aliyuncs.com/%E8%A1%B7%E5%92%8C%E6%A5%BC/16-21%E6%A5%BC/" + framePlayer.get("curFrame") + ".jpg?324324324" ;
            }
            
            // console.log(url);
            var downloadLink = document.createElement("a");
            downloadLink.href = url;
            // downloadLink.download = "imgName.jpg";
            downloadLink.click();
          });


            watch(setfps, (newValue, oldValue) => {
              // 在这里根据 setfps 的变化执行操作
              console.log('新的FPS值为：', newValue);

              framePlayer.set('fps', newValue); // 根据你的 framePlayer 对象进行调整
            });

          }
        });
      })
    })

    const savedLocation = localStorage.getItem('selectedLocation');

    if (savedLocation) {
      selectedLocation.value = savedLocation;
    }

    return {
      setfps,
      selectedLocation,
      saveAndRefresh,
      framePlayer,
      xCoordinate,
      yCoordinate,
    }
  },

  data() {
    return {
      // savedLocation
    };
  },

  methods: {

  },

  mounted() {

  }
}
</script>


<style>
.tools {
  position: relative;
  vertical-align: top;
  text-align: left;
}

.outside-container {
  /* height: 100vh; */
  background-color: red;
}
</style>
