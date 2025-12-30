<template>
	<view>
		<web-view :src="url"></web-view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				// --- CONFIGURATION / 配置 ---
				// IMPORTANT: Replace this with your computer's IP address!
				// 注意：请将此处替换为您电脑的 IP 地址！
				// Example: 'http://192.168.1.5:8501'
				url: 'https://5gx37mny8cenuapfdxetoz.streamlit.app/?embed=true' 
			}
		},
		onLoad() {
			console.log("Entropy God Wrapper Loaded. Target: " + this.url);
		}
	}
</script>

<style>
</style>
