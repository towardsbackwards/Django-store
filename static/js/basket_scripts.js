window.onload = function () {
    /*
    // можем получить DOM-объект меню через JS
    var menu = document.getElementsByClassName('menu')[0];
    menu.addEventListener('click', function () {
        console.log(event);
        event.preventDefault();
    });
    
    // можем получить DOM-объект меню через jQuery
    $('.menu').on('click', 'a', function () {
        console.log('event', event);
        console.log('this', this);
        console.log('event.target', event.target);
        event.preventDefault();
    });
   
    // получаем атрибут href
    $('.menu').on('click', 'a', function () {
        var target_href = event.target.href;
        if (target_href) {
            console.log('нужно перейти: ', target_href);
        }
        event.preventDefault();
    });
    */
    
    // добавляем ajax-обработчик для обновления количества товара
    $('.basket_container').on('change', 'input[type="number"]', function (event) {

        //console.log('Привет');
        console.log('ONCLICK_BASKET_SCRIPTS_RUNNING');
        var target_href = event.target;

        if (target_href) {
        // Пример отправки ajax запроса
            $.ajax({
                url: "/basket/edit/" + target_href.name + "/" + target_href.value + "/",
                // method: 'post',
                //data: {'param': 'pampam'}
                success: function (data) {
                    $('.basket_container').html(data.result);

                    console.log('ajax done');
                },
            });

        }
        event.preventDefault();
    });


    $('.basket_container').on('click', '.inner_delete_button', function (event) {

        console.log('DELETE_BASKET_SCRIPT_RUNNING');
        var target_href = event.target;

        if (target_href) {
        // Пример отправки ajax запроса
            $.ajax({
                url: "/basket/ajaxdelete/" + target_href.name + "/",
                // method: 'post',
                //data: {'param': 'pampam'}
                success: function (data) {
                    $('.basket_container').html(data['result']);
                    console.log('ajax done');
                },
            });

        }
        event.preventDefault();
    });

        $('.basket_list').on('change', 'input[type="number"]', function () {
            console.log('CLICK_SCRIPT IS RUNNED');
        var target_href = event.target;
        console.log(target_href);
        if (target_href) {
            //window.location.href = "/basket/edit/" + target_href.name + "/" + target_href.value + "/";
            $.ajax({
                url: "/basket/edit/" + target_href.name + "/" + target_href.value + "/",

                success: function (data) {
                    $('.basket_list').html(data.result);
                    console.log('ajax done');
                },
            });
        }
        event.preventDefault();
    });
}