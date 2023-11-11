<template>


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
    
    </template>
    
    <script>
    import { Options, Vue } from 'vue-class-component';
    import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src
    import { ElMessage, ElMessageBox } from 'element-plus';
    import { VideoPlay, VideoPause } from '@element-plus/icons-vue';
    import "@/assets/css/style.css"
    import "@/assets/css/font-awesome.min.css"
    import vFramePlayer from '@/assets/js/vframeplayer';
    import $ from 'jquery'
    
    export default {
      data(){
        return{     
    
    
        };
      },
    
      methods:{
        loadImages (Parameter) {
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
    
    
      mounted(){
    
    
        
    
    $(document).ready(function () {
    
        var info = $(".info");
        var process = $(".process");
        var settings = $(".settings");
    
    
        function loadImages (Parameter) {
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
            imgArr.push(require("../assets/image/" + i + ".jpg"));
          }
    
          var dom = document.getElementById("framePlayer");
          console.log(dom);
    
          loadImages({
            loadArr:imgArr,
            complete:function(){
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
                process.css({"width": frame * a + "%"});
    
              });
    
              $(".fa-play").on("click", function () {
                var fps = settings.find(".fps").val();
                var start = settings.find(".start").val();
                var end = settings.find(".end").val();
                framePlayer.play(start, end, {
                  "fps": 4, "yoyo": false, "useCanvas": true, onComplete: function () {
        //                      console.log("完成播放");
                  }, onUpdate: function (frame, times, asc) {
        //                      console.log(frame,times,asc);
                  }
                });
              });
    
              $(".fa-pause").on("click", function () {
                framePlayer.pause();
              });  
              
    
    
            }
          });
    
            
    
    })
    
      }
    
    
    }
    </script>
    