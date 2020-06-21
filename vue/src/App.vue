<template>
  <div id="app">
    <el-row style="width: 100%;height: 50px;background-color: #d88d6d;" class="top">
      <el-col :span="4" :offset="11" style="font-size:20px;font-weight: bold;line-height: 45px">贝叶斯新闻分类</el-col>
    </el-row>

    <el-row class="main">
      <el-col :span="11" :offset="1" style="margin-top: 25px">
        <el-col :span="24">
          <el-tag v-show="label!==''" size="medium" style="margin-right: 5px" type="danger"><i class="el-icon-s-flag"/>&nbsp;{{label}}</el-tag>
          <el-tag :key="tag" v-for="tag in dynamicTags" effect="plain" closable :disable-transitions="false" @close="handleClose(tag)" size="medium" type="info" style="margin-right: 5px;margin-top: 2px;margin-bottom: 5px">{{tag}}</el-tag>
        </el-col>
        <div style="margin: 40px"></div>
        <el-input type="textarea" :autosize="{ minRows: 25,maxRows: 25}" resize="none" placeholder="请输入新闻内容" v-model="textarea1" style="width: 94%;">
        </el-input>
        <div style="margin: 10px"></div>
        <el-col :span="5" :offset="19"><el-button @click="getData" type="primary" round icon="el-icon-s-promotion">提交</el-button></el-col>
      </el-col>
      <el-col :span="1"><div style="width: 0;height: 90vh;border: 1px solid #000000"></div></el-col>
      <el-col :span="11">
        <el-button size="mini" type="primary" style="margin-top: 21px;position: relative;left: 90%" @click="dialogVisible=true">词云</el-button>
        <div style="margin-top:20px"></div>
        <Top :keys="keys" :weight="weight" :change="change"/></el-col>

    </el-row>

    <el-dialog title="提示" :visible.sync="dialogVisible" width="30%">
      <span><el-image :src="imgs"></el-image></span>
    </el-dialog>
  </div>
</template>

<script>
  import {get_data, get_label} from "./request";
  import Top from "./Top";
  export default {
    name: "App",
    components:{Top},
    data(){
      return{
        textarea1:null,
        label:'',
        dynamicTags: [],
        keys:[],
        weight:[],
        change:1,
        dialogVisible: false,
        imgs:''
      }
    },
    created() {
      get_label().then(res=>{
        console.log(res.data);
        this.dynamicTags = res.data
      })
    },
    methods: {
      getData() {
        if (this.textarea1 === null) {
          this.$message.warning('请输入新闻内容')
        } else {
          get_data(this.textarea1).then(res => {
            this.imgs = res.data.url;
            this.dynamicTags = this.dynamicTags.filter(v => v !== res.data.label);
            this.keys = [];
            this.weight = [];
            for (let i of res.data.ten) {
              this.keys.push(i[0]);
              this.weight.push(i[1]);
              this.change++;
            }
            this.label = res.data.label
          })
        }
      },
      handleClose(tag) {
        this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
      },
    }
  }
</script>

<style>
  #app{
    min-width: 1300px;
  }

  .top{
    position: fixed;
    left: 0;
    top: 0;
    right: 0;
  }

  .main{
    margin-top: 60px;
  }
</style>
