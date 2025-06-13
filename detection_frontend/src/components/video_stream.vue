<template>
    <div>
        <h1>Live Video Feed</h1>
        <img :src = "videoSrc" autoplay playsinline/>
        <div class = "stats">
            <p>Total frames processed: {{ stats.frame_count }}</p>
            <p>Total people detected: {{ stats.people_count }}</p>
            <p>Average people per frame: {{ stats.average_people_per_frame }}</p>
        </div>
    </div>
</template>

<script>
import { createWebSocket } from '@/websocket'
export default {
    data() {
        return {
            vidURL:"",
            frameCount_total: 0,
            peopleCount_total: 0,
            averagePeople_total: 0,
            peopleCount_current: 0,
            frameCount_current: 0,
            averagePeople_current: 0,
            socket: null,
            backend_address: '',
        }
    },
    mounted() {
       this.socket = createWebSocket((data) => {
            this.frameCount_total = data.frame_count;
            this.peopleCount_total = data.people_count;
            this.averagePeople_total = data.average_people_per_frame;
            this.frameCount_current = data.current_total_frames;
            this.peopleCount_current = data.current_people_count;
            this.averagePeople_current = data.current_average_people;
            
        });
    },
    beforeunmount() {
        if(this.socket) {
            this.socket.close();
        }
    }
};
</script>