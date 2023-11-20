
<template>
  <div class="card-container" ref="scrollContainer" @scroll="handleScroll">
    <div class="column" v-for="(columnItems, columnIndex) in columns" :key="columnIndex">
      <div v-for="(item, _itemIndex) in columnItems" :key="item.id" class="card-wrapper">
        <el-card :body-style="{ padding: '20px' }">
          <!-- 卡片内容 -->
          <p>{{ item.title }}</p>
          <p>{{ item.description }}</p>
        </el-card>
      </div>
    </div>
    <div v-if="isLoading" class="loading-indicator">Loading...</div>
  </div>
</template>

<style>
.card-container {
  display: flex;
}

.column {
  flex: 1;
  margin-right: 20px;
}

.card-wrapper {
  margin-bottom: 20px;
}

.loading-indicator {
  text-align: center;
}
</style>

<script>
export default {
  data() {
    return {
      columns: [],
      isLoading: false,
    };
  },
  mounted() {
    this.splitItemsIntoColumns();
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    splitItemsIntoColumns() {
      // 你提供的代码
      const items = [
      { id: 1, title: 'Card 1', description: 'Description for Card 1Descra Card 3Description for Card 1Description for Card 1D Card 3Descra Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1Description for Card 1' },
        { id: 2, title: 'Card 2', description: 'Description for Card 2' },
        { id: 3, title: 'Card 3', description: 'Description for Ca Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1Drd 3' },
        { id: 4, title: 'Card 1', description: 'Description for Card 1Description for Card 1' },
        { id: 5, title: 'Card 2', description: 'Description for Card 2' },
        { id: 6, title: 'Card 3', description: 'Description fDescription for Card 1Description for Card 1or Card 3Description for Card 1Description for Card 1Description for Card 1Description for Card 1vDescription for Card 1' },
        { id: 7, title: 'Card 1', description: 'Description for Card 1' },
        { id: 8, title: 'Card 2', description: 'DescriptioDescrip Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1D Card 3Description for Card 1Description for Card 1Dtion for Card 1n for Card 2' },
        { id: 9, title: 'Card 3', description: 'Description for Card 3Description for Card 1Description for Card 1Description for Card 1' },
     
        // ...
      ];

      const numColumns = 3;
      const columnCount = Math.ceil(items.length / numColumns);

      for (let i = 0; i < numColumns; i++) {
        const start = i * columnCount;
        const end = start + columnCount;
        this.columns.push(items.slice(start, end));
      }
    },
    handleScroll() {
      if (this.isLoading) return;
      const scrollContainer = this.$refs.scrollContainer;
      const scrollHeight = scrollContainer.scrollHeight;
      const scrollTop = scrollContainer.scrollTop;
      const clientHeight = scrollContainer.clientHeight;
      const bottomOffset = 20; // 触发加载更多的底部偏移量

      if (scrollTop + clientHeight >= scrollHeight - bottomOffset) {
        this.loadMore();
        console.log("xinshuju")
      }
    },
    loadMore() {
      this.isLoading = true;
      // 模拟异步加载更多数据
      setTimeout(() => {
        const newItems = [
          // 新加载的数据
        ];
        this.columns.push(newItems);
        this.isLoading = false;
      }, 1000);
    },
  },
};
</script>