var mix = {
  methods: {
    setTag(id) {
      this.topTags = this.topTags.map((tag) => {
        if (tag.id === id) {
          tag.selected = !tag.selected;
        } else {
          tag.selected = false;
        }
        return tag;
      });
      this.getCatalogs();
    },
    setSort(id) {
      if (this.selectedSort?.id === id) {
        this.selectedSort.selected =
          this.selectedSort.selected === 'dec' ? 'inc' : 'dec';
      } else {
        if (this.selectedSort) {
          this.selectedSort = null;
        }
        this.selectedSort = this.sortRules.find((sort) => sort.id === id);
        this.selectedSort = {
          ...this.selectedSort,
          selected: 'dec',
        };
      }
      this.getCatalogs();
    },

    getSellers() {
        this.getData('/api/sellers/')
          .then((data) => {
            this.sellers = data;
          })
          .catch(() => {
            this.sellers = [];
            console.warn('Ошибка получения продавцов');
          });
      },
      getSpecifications() {
       const url = '/api/specification/' + this.category + '/';
        this.getData(url)
          .then((data) => {
            this.specifications = data;
            //alert(JSON.stringify(this.specifications));
          })
          .catch(() => {
            this.specifications = [];
            console.warn('Ошибка получения спецификаций');
          });

      },
      getManufacturers() {
        this.getData('/api/manufacturers/')
          .then((data) => {
            this.manufacturers = data;
          })
          .catch(() => {
            this.manufacturers = [];
            console.warn('Ошибка получения производителей');
          });
      },
      updateSpecifications() {

        this.filter.specifications = this.specifications.filter((specification) =>
        this.selectedSpecifications.includes(specification.id)

        );
        //alert(this.filter.specifications);
//        this.filter.specifications = {};
//          if (this.selectedSpecifications && this.selectedSpecifications.length > 0) {
//            for (const { key, value } of this.selectedSpecifications) {
//              if (!this.filter.specifications[key]) {
//                this.filter.specifications[key] = [];
//              }
//              this.filter.specifications[key].push(value);
//            }
//          }
        //alert(this.filter.specifications);
        //this.getCatalogs();
      },
      updateManufacturers() {
        this.filter.manufacturers = this.manufacturers.filter((manufacturer) =>
          this.selectedManufacturers.includes(manufacturer.id)
        );
        //this.getCatalogs();
      },
      updateSellers() {
        this.filter.sellers = this.sellers.filter((seller) =>
          this.selectedSellers.includes(seller.id)
        );
        //this.getCatalogs();
      },
    getTags() {
      this.getData('/api/tags', { category: this.category })
        .then((data) => (this.topTags = data.map((tag) => ({ ...tag, selected: false }))))
        .catch(() => {
          this.topTags = [];
          console.warn('Ошибка получения тегов');
        });
    },
    getCatalogs(page, filterSearch) {
      if (typeof page === 'undefined') {
        page = 1;
      }
      const PAGE_LIMIT = 6;
      const tags = this.topTags
        .filter((tag) => tag.selected)
        .map((tag) => tag.id);
        alert(window.location.search);

       const params = new URLSearchParams(window.location.search);

          // Установка параметров запроса в адресной строке
          params.set('page', page.toString());
            params.set('filterSearch', this.filterSearch ? this.filterSearch : null);
            params.set('category', this.category ? this.category : '');
            params.set('filter.name', this.filter.name);
            params.set('filter.minPrice', this.filter.minPrice.toString());
            params.set('filter.maxPrice', this.filter.maxPrice.toString());
            params.set('filter.freeDelivery', this.filter.freeDelivery.toString());
            params.set('filter.available', this.filter.available.toString());

          if (this.filter.specifications && this.filter.specifications.length > 0) {
            this.filter.specifications.forEach((specification) => {
                  params.append(`filter.specifications.${specification.key}`, specification.value.toString());
            });
          };
          if (this.filter.sellers && this.filter.sellers.length > 0) {
            this.filter.sellers.forEach((seller) => {
             params.append('filter.sellers', seller.toString());
            });
          }
          if (this.filter.manufacturers && this.filter.manufacturers.length > 0) {
            this.filter.manufacturers.forEach((manufacturer) => {
              params.append('filter.manufacturers', manufacturer.toString());
            });
          };

      this.getData('/api/catalog/', {
        page,
        filterSearch: this.filterSearch ? this.filterSearch : null,
        category: this.category ? this.category : null,
        sort: this.selectedSort ? this.selectedSort.id : null,
        sortType: this.selectedSort ? this.selectedSort.selected : null,
        filter: {
          name: this.filter.name ? this.filter.name : null,
          minPrice: this.filter.minPrice ? this.filter.minPrice : null,
          maxPrice: this.filter.maxPrice ? this.filter.maxPrice : null,
          freeDelivery: this.filter.freeDelivery ? this.filter.freeDelivery : null,
          available: this.filter.available ? this.filter.available : null,
          sellers: this.filter.sellers ? this.filter.sellers : null,
          manufacturers: this.filter.manufacturers ? this.filter.manufacturers : null,
          specifications: this.filter.specifications ? this.filter.specifications : null,
        },
        tags,
        limit: PAGE_LIMIT,
      })
        .then(data => {
          this.catalogCards = data.items;
          this.currentPage = data.currentPage;
          this.lastPage = data.lastPage;

          // Обновление адресной строки
          window.history.replaceState(null, null, params.toString());
          params.delete('filter.specifications');

        })
        .catch(() => {
          console.warn('Ошибка при получении каталога');
        });
    },

  },
  mounted() {
    const urlParams = new URL(window.location.href).searchParams;
    //this.filterSearch = urlParams.get('filterSearch');
    this.category = urlParams.get('category') ? Number(urlParams.get('category')) : null;
    this.selectedSort = this.sortRules.find((sort) => sort.id === 'price');
    this.selectedSort.selected = 'inc';
    this.getCatalogs();
    this.getTags();
    this.getSellers();
    this.getManufacturers();
    this.updateSellers();
    this.updateManufacturers();
    this.getSpecifications();
    this.updateSpecifications();

    //this.selectedSellers = []; // список выбранных продавцов
    //this.selectedManufacturers = []; // список выбранных производителей

//    this.category = location.pathname.startsWith('/catalog/')
//        ? Number(location.pathname.replace('/catalog/', '').replace('/', ''))
//        : null;
    //alert(location.pathname.startsWith('/catalog/'));
  },

  data() {
    return {
      pages: 1,
      filterSearch: '',
      category: null,
      catalogCards: [],
      currentPage: null,
      lastPage: 1,
      selectedSort: null,
      filter: {
        name: '',
        minPrice: 1,
        maxPrice: 300000,
        freeDelivery: false,
        available: true,
        sellers: [], // список выбранных продавцов
        manufacturers: [], // список выбранных производителей
        specifications: [],
//        minValue: 0,
//        maxValue: 0,
      },
      sellers: [], // список всех продавцов
      manufacturers: [], // список всех производителей
      specifications: [],
    };
  },
};

