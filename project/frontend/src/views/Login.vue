<template>
    <div class="background">
        <div class="login-form">
            <a-form :model="form">
                <a-form-item label="用户名">
                    <a-input v-model="form.username" @update:value="updateUsername" placeholder="请输入用户名" />
                </a-form-item>
                <a-form-item label="密码">
                    <a-input v-model="form.password" @update:value="updatePassword" type="password" placeholder="请输入密码" />
                </a-form-item>
                <a-form-item>
                    <a-button type="primary" @click="login">登录</a-button>
                </a-form-item>
            </a-form>
        </div>
    </div>
</template>


<script>
import { ref, onMounted } from 'vue';
import { Form, FormItem, Select, SelectOption, Button, Modal, Input, message } from 'ant-design-vue';
import CryptoJS from 'crypto-js';

export default {
    components: {
        AForm: Form,
        AFormItem: FormItem,
        AInput: Input,
        AButton: Button,
    },
    setup() {
        const form = ref({
            username: '',
            password: '',
        });
        const updateUsername = (value) => {
            form.value.username = value;
        };
        const updatePassword = (value) => {
            form.value.password = value;
        };
        const login = () => {
            console.log(`用户名：${form.value.username}`);
            console.log(`密码：${form.value.password}`);
            const hashedPassword = CryptoJS.SHA256(form.value.password).toString();
            console.log(hashedPassword);

            const response = fetch('http://127.0.0.1:5000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: form.value.username,
                    password: hashedPassword,
                }),
            }).then((response) => {
                if (response.status === 200) {
                    response.json().then(data => {
                        const token = data.token;
                        console.log(token);
                        // 你可以在这里保存token，例如保存到localStorage
                        // localStorage.setItem('token', token);
                    });
                    console.log('登录成功');
                    message.success('登录成功');
                    // window.location.href = '/home';
                } else {
                    console.log('登录失败');
                    Modal.error({
                        title: '登录失败',
                        content: '用户名或密码错误',
                    });
                }
            });
        };
        return {
            form,
            updateUsername,
            updatePassword,
            login,
        };
    },
};
</script>


<style>
.background{
    width:100%;
    height:100%;
    position:relative;
    text-align:center;
    color:white;
}

.background::before{    
    content:'';
    position:absolute;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:transparent url("/src/assets/img/background.png") center center no-repeat;
    background-size:cover;
    z-index: -1;
}

.login-form{
    width: 400px;
    height: 100%;
    float: right;
    display: flex;
    justify-content: center;

    background-color: #ffffff;
    /* border-radius: 10px;
    box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.15); */
    padding: 30px;
}
</style>
