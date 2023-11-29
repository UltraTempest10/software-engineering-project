<template>
  <div class="intro">
    <span class="intro-title">图片播放</span>
    <div class="block-container">
      <Feature
        :image="require('@/assets/img/camera.png')"
        title="可调节帧数"
        description="提供高清晰度的玻璃幕墙动态图片，让用户可以清晰地观察细节。"
      />
      <Feature
        :image="require('@/assets/img/drone.png')"
        title="全方位拍摄"
        description="通过无人机进行全方位拍摄，仔细检查每一部分的外立面。"
      />
    </div>
  </div>
  <el-container class="main">
  
    <el-aside>
      <div class="tools">
        <!-- <el-row> -->
          <!-- <el-icon style="font-size: 32px;">
            <Camera />
          </el-icon> -->
        <!-- </el-row> -->
        <label class="tool-item">
          <span>FPS:</span>
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
          <span>拍摄位置:</span>
          <el-form-item>
            <el-select v-model="selectedLocation" placeholder="请选择拍摄位置">
              <el-option label="衷和楼10-15楼" value="衷和楼10-15楼" />
            </el-select>
          </el-form-item>
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
            <div class="process_bar">
              <div class="process"></div>
            </div>
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
    const selectedLocation = ref('');

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

        var imgArr = [];

        for (var i = 0; i < 90; i++) {
          imgArr.push("https://curtain-wall.oss-cn-shanghai.aliyuncs.com/low-res/" + i + ".jpg?324324324");
        }

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

            watch(setfps, (newValue, oldValue) => {
              // 在这里根据 setfps 的变化执行操作
              console.log('新的FPS值为：', newValue);

              framePlayer.set('fps', newValue); // 根据你的 framePlayer 对象进行调整
            });

            /*
            watch(selectedLocation, (newValue, oldValue) => {
              // 在这里根据 setfps 的变化执行操作
              
              var newImgArr = [];
        
              // 根据不同的位置值加载不同的图片资源
              if (newValue === '衷和楼10-15楼') {
                for (var i = 0; i < 90; i++) {
                  newImgArr.push("https://curtain-wall.oss-cn-shanghai.aliyuncs.com/low-res/" + i + ".jpg");
                }
              } else if (newValue === '衷和楼16-21楼') {
                for (var i = 0; i < 89; i++) {
                  newImgArr.push("https://curtain-wall.oss-cn-shanghai.aliyuncs.com/%E8%A1%B7%E5%92%8C%E6%A5%BC/16-21%E6%A5%BC/" + i + ".jpg");
                }
              }
        
              // 清空原有的图片资源数组
              imgArr.splice(0, imgArr.length);
              // 将新的图片资源数组赋值给 imgArr
              imgArr.push(...newImgArr);
            });
        */
          }
        });
      })
    })

    return {
      setfps,
      selectedLocation
    }
  },

  data() {
    return {
      selectedLocation: '衷和楼10-15楼', // 设置默认值
    };
  },

  methods: {
    loadImages(Parameter) {
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
    },
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

.el-container {
  .el-aside {
    border-radius: 10px;
    box-shadow: 0px 0px 8px rgba(10, 10, 10, 0.3);
    padding: 20px;
    width: 480px;
    text-align: center;
  }

  .el-main {
    display: flex;
    justify-content: right;
    align-items: center;
  }

  .el-form-item {
    margin-bottom: 0px;
  }
}

.outside-container {
  /* height: 100vh; */
  background-color: red;
}
</style>
