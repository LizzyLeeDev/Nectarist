// = = = = = = = = = = = = = = = = = = = = = = = = = = =
// 공통
// = = = = = = = = = = = = = = = = = = = = = = = = = = =

    // TEXTAREA 크기조정
    $("textarea").on("input", function () {
        $(this).height(0);
        $(this).height(this.scrollHeight);
    });

    // CKEDITOR
    if($("#nectarist_form_text").length > 0){
        CKEDITOR.replace("nectarist_form_text", {
            enterMode: CKEDITOR.ENTER_BR,
            shiftEnterMode: CKEDITOR.ENTER_P,
            fillEmptyBlocks: false
        });
    }

    // SELECT2 드롭다운 이슈 수정
    $(".select2").select2({dropdownParent: $("#container_center"), width: "100%"});
    $(function () {
        $(".select2").on("select2:open, keyup, focus, click, change", function () {
            select2resize();
        });
        $(".select2-selection").on("select2:open, keyup, focus", function () {
            setTimeout(() => select2resize(), 500);
        });
    });
    $(window).on("resize", function () {
        select2resize();
    });
    function select2resize() {
        $(".select2-dropdown").parent().width($(".select2-dropdown").width() + 2);
        $(".select2-dropdown").parent().height($(".select2-dropdown").height() + 2);
    }

    // 부트스트랩 툴팁
    $("[data-bs-toggle='tooltip']").each(function (idx, obj) {
        new bootstrap.Tooltip(obj)
    });

    // 모달 닫기
    $(".modal-close").on("click", function () {
        $(this).parents(".modal").modal("hide");
    })

// = = = = = = = = = = = = = = = = = = = = = = = = = = =
// 공통 - 냉장고 (칵테일계산기 + 마이페이지 - 내 냉장고)
// = = = = = = = = = = = = = = = = = = = = = = = = = = =

    // 냉장고 - 비어있음 처리
    if($("#nectarist_refrig_container .nectarist-ingrd-item").length == 0){
        $("#nectarist_ingrd_empty").removeClass("d-none");
    }

    // 냉장고 - 재료 삭제 저장
    var deleteIngrd = [];
    $(function () {
        $("#nectarist_refrig_container").on("click", ".nectarist-ingrd-delete", function () {
            var ino = $(this).closest(".nectarist-ingrd-item").attr("data-ingno");
            deleteIngrd.push(ino);
            $(this).closest(".nectarist-ingrd-item").remove();

            if($("#nectarist_refrig_container .nectarist-ingrd-item").length == 0){
                $("#nectarist_ingrd_empty").removeClass("d-none");
            }
        });
    });

    // 냉장고 - 재료 추가
    function req_refrig_add(){
        var selectedIngrd = $("#nectarist_refrig_ingrd").val();
        if(selectedIngrd.length > 0){
            selectedIngrd.forEach(function(ingrdNo) {
                // 현재 냉장고에 없는 것만 추가 가능하도록 처리
                if($("#nectarist_refrig_container .nectarist-ingrd-item[data-ingno='" + ingrdNo + "']").length == 0){
                    var ingrdOption = $("#nectarist_refrig_ingrd option[value='" + ingrdNo + "']");
                    var ingrdType = $(ingrdOption).attr("data-type");
                    var ingrdName = $(ingrdOption).text();
                    var ingrdSrc = "";
                    ingrdSrc += "<div class='nectarist-ingrd-item' data-ingno='" + ingrdNo + "'>";
                    ingrdSrc += "<span class='nectarist-ingrd-type'>";
                    switch(ingrdType){
                        case "01":
                            ingrdSrc += "<i class='fa fa-bottle-droplet'></i>";
                        break;
                        case "02":
                            ingrdSrc += "<i class='fa fa-glass-water'></i>";
                        break;
                        case "03":
                            ingrdSrc += "<i class='fa fa-cubes-stacked'></i>";
                        break;
                    }
                    ingrdSrc += "</span>";
                    ingrdSrc += "<span class='nectarist-ingrd-name'>" + ingrdName + "</span>";
                    ingrdSrc += "<span class='nectarist-ingrd-delete'><i class='fa fa-xmark'></i></span>";
                    $("#nectarist_refrig_container").append(ingrdSrc);
                }
            });
        }
        $("#nectarist_ingrd_empty").addClass("d-none");
        $("#nectarist_refrig_ingrd").val([]).change();
    }

    // 냉장고 - 재료 저장
    function req_refrig_save(){
        var selectedIngrd = [];
        $("#nectarist_refrig_container .nectarist-ingrd-item").each(function (idx, obj) {
            selectedIngrd.push($(obj).attr("data-ingno"));
        });
        var saveRefrigData = {
            "selected": selectedIngrd.join(','),
            "deleted": deleteIngrd.join(',')
        }
        $.ajax({
            url: "/mypage_myrefrig/req_saverefrig",
            data: saveRefrigData,
            dataType: "json",
            success: function (result) {
                if(result.save_refrig_result == "Y"){
                    location.reload();
                }
                else {
                    swal({
                        title: "냉장고 저장 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })
    }

    // 냉장고 - 칵테일 계산
    function req_refrig_calc(){
        var selectedIngrd = [];
        $("#nectarist_refrig_container .nectarist-ingrd-item").each(function (idx, obj) {
            selectedIngrd.push($(obj).attr("data-ingno"));
        });
        // 없는 경우
        if(selectedIngrd.length == 0) {
            swal({
                text: "재료를 1개 이상 선택해주세요.",
                icon: "warning"
            });
        }
        else {
            // 체크된 경우 저장
            if($("#nectarist_refrig_savechk").prop("checked")){
                var saveRefrigData = {
                    "selected": selectedIngrd.join(','),
                    "deleted": deleteIngrd.join(',')
                }
                $.ajax({
                    url: "/mypage_myrefrig/req_saverefrig/",
                    data: saveRefrigData,
                    dataType: "json",
                    success: function (result) {
                        if(result.save_refrig_result != "Y"){
                            swal({
                                title: "냉장고 저장 실패",
                                text: "잘못된 접근입니다.",
                                icon: "warning"
                            });
                        }
                    }
                })

            }
            // 계산 정보와 함께 이동(POST)
            $("#nectarist_refrig_form").find("input").val(selectedIngrd.join(','));
            $("#nectarist_refrig_form").submit();
        }
    }

// = = = = = = = = = = = = = = = = = = = = = = = = = = =
// 일반 카테고리
// = = = = = = = = = = = = = = = = = = = = = = = = = = =

    // 칵테일정보 - 칵테일등록 - 재료추가
    function req_cocktailinfo_addingrdnt(btn){
        var ingObj = $(btn).prev(".cocktail-ingrdnt-item")[0].outerHTML;
        $(ingObj).insertBefore(btn);

        // 버튼 활성화
        $(".cocktail-ingrdnt-item .cocktail-ingrdnt-item-del").prop("disabled", false);
    }

    // 칵테일정보 - 칵테일등록 - 재료삭제
    $("#nectarist_cocktailinfo_ingcontainer").on("click", ".cocktail-ingrdnt-item-del", function () {
        $(this).parents(".cocktail-ingrdnt-item").remove();

        // 한개인 경우 버튼 비활성화
        if($("#nectarist_cocktailinfo_ingcontainer").find(".cocktail-ingrdnt-item").length == 1){
            $("#nectarist_cocktailinfo_ingcontainer .cocktail-ingrdnt-item-del").prop("disabled", true);
        }
    })

    // 칵테일정보 - 칵테일등록 - 신규추가
    function req_cocktailinfo_addsave() {
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
        var addCocktailData = new FormData();
        addCocktailData.append("name", $("#nectarist_cocktailinfo_name").val());
        addCocktailData.append("engname", $("#nectarist_cocktailinfo_engname").val());
        addCocktailData.append("recipe", $("#nectarist_cocktailinfo_recipe").val());
        addCocktailData.append("memo", $("#nectarist_cocktailinfo_memo").val());
        // 섬네일
        if($("#nectarist_cocktailinfo_thumbnail").length > 0){
            addCocktailData.append("thumbnail", $("#nectarist_cocktailinfo_thumbnail")[0].files[0]);
        }
        else{
            addCocktailData.append("thumbnail", "");
        }
        // 재료
        var ingList = [];
        $("#nectarist_cocktailinfo_ingcontainer").find(".cocktail-ingrdnt-item").each(function () {
            var ingObj = {};
            ingObj["ingrdnt"] = $(this).find(".nectarist-cocktailinfo-ingrdnt").val();
            ingObj["amt"] = $(this).find(".nectarist-cocktailinfo-quant").val();
            ingObj["unit"] = $(this).find(".nectarist-cocktailinfo-unit").val();
            ingList.push(ingObj);
        })
        addCocktailData.append("ingrdnt", JSON.stringify(ingList));
        $.ajax({
            url: "/cocktailinfo/req_saveaddcocktail",
            data: addCocktailData,
            type: "post",
            headers: {"X-CSRFToken": csrftoken},
            dataType: "json",
            processData: false,
            contentType: false,
            success: function (result) {
                if(result.add_result == "Y"){
                    location.href = "/cocktailinfo/detail/" + result.cocktail_id;
                }
                else {
                    swal({
                        title: "칵테일 정보 추가 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })
    }

    // 칵테일정보 - 칵테일등록 - 수정
    function req_cocktailinfo_modsave(cno) {
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
        var modCocktailData = new FormData();
        modCocktailData.append("cno", cno);
        modCocktailData.append("name", $("#nectarist_cocktailinfo_name").val());
        modCocktailData.append("engname", $("#nectarist_cocktailinfo_engname").val());
        modCocktailData.append("recipe", $("#nectarist_cocktailinfo_recipe").val());
        modCocktailData.append("memo", $("#nectarist_cocktailinfo_memo").val());
        // 섬네일
        if($("#nectarist_cocktailinfo_thumbnail").length > 0){
            modCocktailData.append("thumbnail", $("#nectarist_cocktailinfo_thumbnail")[0].files[0]);
        }
        else{
            modCocktailData.append("thumbnail", "");
        }
        // 재료
        var ingList = [];
        $("#nectarist_cocktailinfo_ingcontainer").find(".cocktail-ingrdnt-item").each(function () {
            var ingObj = {};
            ingObj["ingrdnt"] = $(this).find(".nectarist-cocktailinfo-ingrdnt").val();
            ingObj["amt"] = $(this).find(".nectarist-cocktailinfo-quant").val();
            ingObj["unit"] = $(this).find(".nectarist-cocktailinfo-unit").val();
            ingList.push(ingObj);
        })
        modCocktailData.append("ingrdnt", JSON.stringify(ingList));
        $.ajax({
            url: "/cocktailinfo/req_savemodcocktail",
            data: modCocktailData,
            type: "post",
            headers: {"X-CSRFToken": csrftoken},
            dataType: "json",
            processData: false,
            contentType: false,
            success: function (result) {
                if(result.mod_result == "Y"){
                    location.href = "/cocktailinfo/detail/" + cno;
                }
                else {
                    swal({
                        title: "칵테일 정보 수정 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })
    }

    // 칵테일정보 - 삭제 버튼
    function req_cocktailinfo_del(cno){
        swal({
            title: "칵테일 정보 삭제",
            text: "해당 칵테일 정보를 삭제합니다.",
            icon: "warning",           
            buttons: ["취소", "확인"]
        }).then((btnResult) => {
            if(btnResult){
                $.ajax({
                    url: "/cocktailinfo/req_delcocktail",
                    data: {"cno": cno},
                    dataType: "json",
                    success: function (result) {
                        if(result.del_result == "Y"){
                            location.href = "/cocktailinfo/?page=1";
                        }
                        else {
                            swal({
                                title: "칵테일 정보 삭제 실패",
                                text: "잘못된 접근입니다.",
                                icon: "warning"
                            });
                        }
                    }
                })
            }
        });
    }

    // 칵테일정보 - 댓글등록
    function req_add_cocktail_comment(cno) {
        var addCommentData = {
            "cno": cno,
            "text": $("#nectarist_comment_input").val()
        }
        $.ajax({
            url: "/cocktailinfo/req_addcktcmt/",
            data: addCommentData,
            dataType: "json",
            success: function (result) {
                if(result.add_comment_result == "Y"){
                    location.reload();
                }
                else {
                    swal({
                        title: "댓글 추가 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })
    }

    // 칵테일정보 - 댓글삭제
    function req_cocktail_comment_del(cmno) {
        swal({
            title: "댓글 삭제",
            text: "해당 댓글을 삭제합니다.",
            icon: "warning",           
            buttons: ["취소", "확인"]
        }).then((btnResult) => {
            if(btnResult){
                $.ajax({
                    url: "/cocktailinfo/req_delcktcmt/",
                    data: {"cmno": cmno},
                    dataType: "json",
                    success: function (result) {
                        if(result.del_result == "Y"){
                            location.reload();
                        }
                        else {
                            swal({
                                title: "댓글 삭제 실패",
                                text: "잘못된 접근입니다.",
                                icon: "warning"
                            });
                        }
                    }
                })
            }
        });
    }

    // 칵테일정보 - 댓글수정 저장
    function req_cocktail_comment_modsave(btn, cmno) {
        var commentItem = $(btn).parents(".nectarist-comment-item");
        var modCommentData = {
            "cmno": cmno,
            "text": $(commentItem).find(".nectarist-comment-mod-input").val()
        }
        $.ajax({
            url: "/cocktailinfo/req_modcktcmt//",
            data: modCommentData,
            dataType: "json",
            success: function (result) {
                if(result.mod_comment_result == "Y"){
                    location.reload();
                }
                else {
                    swal({
                        title: "댓글 수정 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })
    }

    // 게시판 - 글등록
    function req_board_new(boardType, boardlink){
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
        var addBoardData = new FormData();
        addBoardData.append("type", boardType);
        addBoardData.append("title", $("#nectarist_form_title").val());
        addBoardData.append("text", CKEDITOR.instances.nectarist_form_text.getData());
        // 섬네일
        if($("#nectarist_form_thumbnail").length > 0){
            addBoardData.append("thumbnail", $("#nectarist_form_thumbnail")[0].files[0]);
        }
        // 태그
        if($(".nectarist-form-select").val() != null){
            addBoardData.append("tag", $(".nectarist-form-select").val().join(','));
        }
        else {
            addBoardData.append("tag", "");
        }
        $.ajax({
            url: "/req_addbrd/",
            data: addBoardData,
            type: "post",
            headers: {"X-CSRFToken": csrftoken},
            dataType: "json",
            processData: false,
            contentType: false,
            success: function (result) {
                if(result.add_board_result == "Y"){
                    location.href = boardlink + "/detail/" + result.board_id;
                }
                else {
                    swal({
                        title: "게시글 추가 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })
    }

    // 게시판 - 삭제 버튼
    function req_board_del(bno, boardlink){
        swal({
            title: "게시글 삭제",
            text: "해당 게시글을 삭제합니다.",
            icon: "warning",           
            buttons: ["취소", "확인"]
        }).then((btnResult) => {
            if(btnResult){
                $.ajax({
                    url: "/req_delbrd",
                    data: {"bno": bno},
                    dataType: "json",
                    success: function (result) {
                        if(result.del_result == "Y"){
                            location.href = "/" + boardlink + "/?page=1";
                        }
                        else {
                            swal({
                                title: "게시글 삭제 실패",
                                text: "잘못된 접근입니다.",
                                icon: "warning"
                            });
                        }
                    }
                })
            }
        });
    }

    // 게시판 - 수정
    function req_board_modsave(boardType, boardlink, bno){
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
        var modBoardData = new FormData();
        modBoardData.append("bno", bno);
        modBoardData.append("type", boardType);
        modBoardData.append("title", $("#nectarist_form_title").val());
        modBoardData.append("text", CKEDITOR.instances.nectarist_form_text.getData());
        // 섬네일
        if($("#nectarist_form_thumbnail").length > 0){
            modBoardData.append("thumbnail", $("#nectarist_form_thumbnail")[0].files[0]);
        }
        // 태그
        if($(".nectarist-form-select").val() != null){
            modBoardData.append("tag", $(".nectarist-form-select").val().join(','));
        }
        else {
            modBoardData.append("tag", "");
        }
        $.ajax({
            url: "/req_modbrd/",
            data: modBoardData,
            type: "post",
            headers: {"X-CSRFToken": csrftoken},
            dataType: "json",
            processData: false,
            contentType: false,
            success: function (result) {
                if(result.mod_board_result == "Y"){
                    location.href = boardlink + "/detail/" + bno;
                }
                else {
                    swal({
                        title: "게시글 수정 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })

    }

    // 게시판 - 댓글등록
    function req_add_board_comment(bno) {
        var addCommentData = {
            "bno": bno,
            "text": $("#nectarist_comment_input").val()
        }
        $.ajax({
            url: "/req_addbrdcmt/",
            data: addCommentData,
            dataType: "json",
            success: function (result) {
                if(result.add_comment_result == "Y"){
                    location.reload();
                }
                else {
                    swal({
                        title: "댓글 추가 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })

    }

    // 게시판 - 댓글삭제
    function req_comment_del(cmno) {
        swal({
            title: "댓글 삭제",
            text: "해당 댓글을 삭제합니다.",
            icon: "warning",           
            buttons: ["취소", "확인"]
        }).then((btnResult) => {
            if(btnResult){
                $.ajax({
                    url: "/req_delcomment",
                    data: {"cmno": cmno},
                    dataType: "json",
                    success: function (result) {
                        if(result.del_result == "Y"){
                            location.reload();
                        }
                        else {
                            swal({
                                title: "댓글 삭제 실패",
                                text: "잘못된 접근입니다.",
                                icon: "warning"
                            });
                        }
                    }
                })
            }
        });
    }

    // 게시판 - 댓글수정
    function req_comment_mod(btn) {
        var commentItem = $(btn).parents(".nectarist-comment-item");
        $(commentItem).find(".nectarist-comment-mod-input").val($(commentItem).find(".nectarist-comment-text").text());
        $(commentItem).find(".nectarist-comment-text").addClass("d-none");
        $(commentItem).find(".nectarist-comment-time").addClass("d-none");
        $(commentItem).find(".nectarist-comment-button").addClass("d-none");
        $(commentItem).find(".nectarist-comment-mod-input").removeClass("d-none");
        $(commentItem).find(".nectarist-comment-mod-button").removeClass("d-none");
    }

    // 게시판 - 댓글수정 저장
    function req_comment_modsave(btn, cmno) {
        var commentItem = $(btn).parents(".nectarist-comment-item");
        var modCommentData = {
            "cmno": cmno,
            "text": $(commentItem).find(".nectarist-comment-mod-input").val()
        }
        $.ajax({
            url: "/req_modcomment/",
            data: modCommentData,
            dataType: "json",
            success: function (result) {
                if(result.mod_comment_result == "Y"){
                    location.reload();
                }
                else {
                    swal({
                        title: "댓글 수정 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })
    }

// = = = = = = = = = = = = = = = = = = = = = = = = = = =
// 로그인
// = = = = = = = = = = = = = = = = = = = = = = = = = = =

    // 회원가입 - ID 입력검사
    $("#nectarist_form_signup_id").on("input", function () {
        $(".nectarist_form_id_result").addClass("d-none");
        $("#nectarist_form_signup_id").attr("data-valid", "N");
        $("#nectarist_form_signup_id").removeClass("invalid-input");
    })

    // 회원가입 - ID 중복확인
    function req_duplicate_id(){
        var inputid = $("#nectarist_form_signup_id").val();
        
        if(/^[a-z0-9]*$/.test(inputid) && inputid.length >= 6 && inputid.length <= 12) {
            $.ajax({
                url: "/sign_up/req_dupid/",
                data: {"inputid": inputid},
                dataType: "json",
                success: function (result) {
                    if(result.is_duplicate == "N") {
                        $("#nectarist_form_signup_id").attr("data-valid", "Y");
                        $("#nectarist_form_signup_id").removeClass("invalid-input");
                        $("#nectarist_form_okid").removeClass("d-none");
                    }
                    else {
                        $("#nectarist_form_dupid").removeClass("d-none");
                    }
                }
            })
        }
        else {
            $("#nectarist_form_invalidid").removeClass("d-none");
        }
    }

    // 회원가입 - 비밀번호 입력검사
    $("#nectarist_form_signup_pw").on("input", function () {
        var inputpw = $("#nectarist_form_signup_pw").val();
        
        $(".nectarist_form_pw_result").addClass("d-none");
        $("#nectarist_form_signup_pw").attr("data-valid", "N");
        $("#nectarist_form_signup_pw").removeClass("invalid-input");

        if(/^[a-z0-9!@#$%^&*]*$/.test(inputpw) && inputpw.length >= 10 && inputpw.length <= 20) {
            $("#nectarist_form_signup_pw").attr("data-valid", "Y");
            $("#nectarist_form_okpw").removeClass("d-none");
        }
        else {
            $("#nectarist_form_invalidpw").removeClass("d-none");
        }
    })

    // 회원가입 - 비밀번호 확인 입력검사
    $("#nectarist_form_signup_pwchk").on("input", function () {
        var inputpwchk = $("#nectarist_form_signup_pwchk").val();
        
        $(".nectarist_form_pwchk_result").addClass("d-none");
        $("#nectarist_form_signup_pwchk").attr("data-valid", "N");
        $("#nectarist_form_signup_pwchk").removeClass("invalid-input");

        if(inputpwchk == $("#nectarist_form_signup_pw").val()) {
            $("#nectarist_form_signup_pwchk").attr("data-valid", "Y");
            $("#nectarist_form_okpwchk").removeClass("d-none");
        }
        else {
            $("#nectarist_form_invalidpwchk").removeClass("d-none");
        }
    })

    // 회원가입 - 닉네임 입력검사
    $("#nectarist_form_signup_name").on("input", function () {
        $(".nectarist_form_name_result").addClass("d-none");
        $("#nectarist_form_signup_name").attr("data-valid", "N");
        $("#nectarist_form_signup_name").removeClass("invalid-input");
    })

    // 회원가입 - 닉네임 중복확인
    function req_duplicate_name(){
        var inputname = $("#nectarist_form_signup_name").val();

        if(inputname.length >= 2 && inputname.length <= 10) {
            $.ajax({
                url: "/sign_up/req_dupname/",
                data: {"inputname": inputname},
                dataType: "json",
                success: function (result) {
                    if(result.is_duplicate == "N") {
                        $("#nectarist_form_signup_name").attr("data-valid", "Y");
                        $("#nectarist_form_signup_name").removeClass("invalid-input");
                        $("#nectarist_form_okname").removeClass("d-none");
                    }
                    else {
                        $("#nectarist_form_dupname").removeClass("d-none");
                    }
                }
            })
        }
        else {
            $("#nectarist_form_invalidname").removeClass("d-none");
        }
    }

    // 회원가입 - 이메일 입력검사
    $("#nectarist_form_signup_email").on("input", function () {
        var inputpwemail = $("#nectarist_form_signup_email").val();
        
        $(".nectarist_form_email_result").addClass("d-none");
        $("#nectarist_form_signup_email").attr("data-valid", "N");
        $("#nectarist_form_signup_email").removeClass("invalid-input");

        if(/^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-Za-z0-9\-]+/.test(inputpwemail)) {
            $("#nectarist_form_signup_email").attr("data-valid", "Y");
            $("#nectarist_form_okemail").removeClass("d-none");
        }
        else {
            $("#nectarist_form_invalidemail").removeClass("d-none");
        }
    })

    // 회원가입 - 회원가입 요청
    function req_signup() {
        $(".invalid-input").removeClass("invalid-input");
        
        if($("#nectarist_form_signup_id").attr("data-valid") == "N"){
            $("#nectarist_form_signup_id").addClass("invalid-input");
        }
        if($("#nectarist_form_signup_pw").attr("data-valid") == "N"){
            $("#nectarist_form_signup_pw").addClass("invalid-input");
        }
        if($("#nectarist_form_signup_pwchk").attr("data-valid") == "N"){
            $("#nectarist_form_signup_pwchk").addClass("invalid-input");
        }
        if($("#nectarist_form_signup_name").attr("data-valid") == "N"){
            $("#nectarist_form_signup_name").addClass("invalid-input");
        }
        if($("#nectarist_form_signup_email").attr("data-valid") == "N"){
            $("#nectarist_form_signup_email").addClass("invalid-input");
        }

        var invalid = $(".nectarist-form .invalid-input").length;
        if(invalid == 0){
            var signUpData = {
                "id": $("#nectarist_form_signup_id").val(),
                "pw": $("#nectarist_form_signup_pw").val(),
                "name": $("#nectarist_form_signup_name").val(),
                "email": $("#nectarist_form_signup_email").val()
            }
            $.ajax({
                url: "/sign_up/req_signup/",
                data: signUpData,
                dataType: "json",
                success: function (result) {
                    if(result.sign_up_result == "Y"){
                        swal({
                            title: "회원가입 완료",
                            text: "로그인 화면으로 이동합니다.",
                            closeOnClickOutside: false,
                            closeOnEsc: false,
                            icon: "success",
                            button: "확인",
                        }).then((value) => {
                            location.href = "/sign_in/"
                        });
                    }
                    else {
                        swal({
                            title: "회원가입 실패",
                            text: "관리자 문의 바랍니다.",
                            icon: "warning"
                        });
                    }
                }
            })
        }
    }

    // 로그인 - 엔터 로그인 처리
    $("#nectarist_signin_pw").on("keyup", function (e) {
        if(e.keyCode == 13) req_signin();
    });

    // 로그인 - 로그인 요청
    function req_signin() {
        var signInData = {
            "id": $("#nectarist_signin_id").val(),
            "pw": $("#nectarist_signin_pw").val()
        }
        $.ajax({
            url: "req_signin",
            data: signInData,
            dataType: "json",
            success: function (result) {
                if(result.sign_in_result == "Y"){
                    location.href = "/";
                }
                else {
                    swal({
                        title: "로그인 실패",
                        text: "잘못된 회원정보입니다.",
                        icon: "warning"
                    });
                }
            }
        })
    }

    // 아이디 찾기 - 이메일 입력검사
    $("#nectarist_form_findid_email").on("input", function () {
        var inputidemail = $("#nectarist_form_findid_email").val();
        
        $(".nectarist_form_email_result").addClass("d-none");
        $("#nectarist_form_findid_email").attr("data-valid", "N");
        $("#nectarist_button_findid").addClass("disabled");

        if(/^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-Za-z0-9\-]+/.test(inputidemail)) {
            $("#nectarist_form_findid_email").attr("data-valid", "Y");
            $("#nectarist_form_okemail").removeClass("d-none");
            $("#nectarist_button_findid").removeClass("disabled");
        }
        else {
            $("#nectarist_form_invalidemail").removeClass("d-none");
        }
    })

    // 아이디 찾기 - 아이디 검색
    function req_findid() {
        if($("#nectarist_form_findid_email").attr("data-valid") == "Y"){
            var inputemail = $("#nectarist_form_findid_email").val();
            $.ajax({
                url: "/find_id/req_findid/",
                data: {"inputemail": inputemail},
                dataType: "json",
                success: function (result) {
                    $("#nectarist_form_findid_result").addClass("d-none");
                    $("#nectarist_form_findid_result").removeClass("d-inline-block");
                    $("#nectarist_form_findid_none").addClass("d-none");
                    $("#nectarist_form_findid_none").removeClass("d-inline-block");

                    if(result.is_id_exist == "Y"){
                        $("#nectarist_form_findid_result").html("회원님의 아이디는 <span class='font-weight-bold text-danger'>**" + result.ret_id.substring(2) + "</span> 으로 등록되어있습니다.")
                        $("#nectarist_form_findid_result").removeClass("d-none");
                        $("#nectarist_form_findid_result").addClass("d-inline-block");
                    }
                    else {
                        $("#nectarist_form_findid_none").removeClass("d-none");
                        $("#nectarist_form_findid_none").addClass("d-inline-block");
                    }
                }
            })
        }
    }

    // 비밀번호 찾기 - 아이디 입력검사
    $("#nectarist_form_findpw_id").on("input", function () {
        var inputpwid = $("#nectarist_form_findpw_id").val();

        $("#nectarist_form_invalidid").addClass("d-none");
        $("#nectarist_form_findpw_id").attr("data-valid", "N");
        $("#nectarist_button_findpw").addClass("disabled");

        if(/^[a-z0-9]*$/.test(inputpwid) && inputpwid.length >= 6 && inputpwid.length <= 12) {
            $("#nectarist_form_findpw_id").attr("data-valid", "Y");
            if($("#nectarist_form_findpw_email").attr("data-valid") == "Y") {
                $("#nectarist_button_findpw").removeClass("disabled");
            }
        }
        else {
            $("#nectarist_form_invalidid").removeClass("d-none");
        }
    })

    // 비밀번호 찾기 - 이메일 입력검사
    $("#nectarist_form_findpw_email").on("input", function () {
        var inputidemail = $("#nectarist_form_findpw_email").val();
        
        $(".nectarist_form_email_result").addClass("d-none");
        $("#nectarist_form_findpw_email").attr("data-valid", "N");
        $("#nectarist_button_findpw").addClass("disabled");

        if(/^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-Za-z0-9\-]+/.test(inputidemail)) {
            $("#nectarist_form_findpw_email").attr("data-valid", "Y");
            if($("#nectarist_form_findpw_id").attr("data-valid") == "Y") {
                $("#nectarist_button_findpw").removeClass("disabled");
            }
        }
        else {
            $("#nectarist_form_invalidemail").removeClass("d-none");
        }
    })

    // 비밀번호 찾기 - 비밀번호 찾기
    function req_findpw() {
        if($("#nectarist_form_findpw_id").attr("data-valid") == "Y" && $("#nectarist_form_findpw_email").attr("data-valid") == "Y"){
            var inputid = $("#nectarist_form_findpw_id").val();
            var inputemail = $("#nectarist_form_findpw_email").val();
            $.ajax({
                url: "/find_pw/req_findpw/",
                data: {"inputid": inputid, "inputemail": inputemail},
                dataType: "json",
                success: function (result) {
                    $("#nectarist_form_findpw_none").addClass("d-none");
                    $("#nectarist_form_findpw_none").removeClass("d-inline-block");
                    $("#nectarist_form_findpw_result").addClass("d-none");
                    $("#nectarist_form_findpw_result").removeClass("d-inline-block");

                    if(result.is_id_exist == "Y"){
                        $("#nectarist_form_findpw_result").removeClass("d-none");
                        $("#nectarist_form_findpw_result").addClass("d-inline-block");
                    }
                    else {
                        $("#nectarist_form_findpw_none").removeClass("d-none");
                        $("#nectarist_form_findpw_none").addClass("d-inline-block");
                    }
                }
            })
        }
    }

    // 로그아웃 요청
    function req_signout() {
        $.ajax({
            url: "/req_signout",
            dataType: "json",
            success: function (result) {
                if(result.sign_out_result == "Y"){
                    location.href = "/";
                }
                else {
                    swal({
                        title: "로그아웃 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })
    }

// = = = = = = = = = = = = = = = = = = = = = = = = = = =
// 마이페이지
// = = = = = = = = = = = = = = = = = = = = = = = = = = =

    // 내정보 관리 - 닉네임 변경버튼
    $("#nectarist_myinfo_changename").on("click", function () {
        $(".nectarist-myinfo-befchange").addClass("d-none");
        $(".nectarist-myinfo-afchange").removeClass("d-none");
    })

    // 내정보 관리 - 닉네임 변경요청
    function req_mynickname(){
        $(".invalid-input").removeClass("invalid-input");
        
        // 닉네임 변경 불가
        if($("#nectarist_form_signup_name").attr("data-valid") == "N"){
            $("#nectarist_form_signup_name").addClass("invalid-input");
        }
        // 닉네임 변경
        else{
            var nameData = {
                "name": $("#nectarist_form_signup_name").val()
            }
            $.ajax({
                url: "/mypage_myinfo/req_namechange",
                data: nameData,
                dataType: "json",
                success: function (result) {
                    if(result.change_result == "Y"){
                        swal({
                            title: "닉네임 변경 완료",
                            closeOnClickOutside: false,
                            closeOnEsc: false,
                            icon: "success",
                            button: "확인",
                        }).then((value) => {
                            location.reload();
                        });
                    }
                    else {
                        swal({
                            title: "닉네임 변경 실패",
                            text: "관리자 문의 바랍니다.",
                            icon: "warning"
                        });
                    }
                }
            })

        }

    }

    // 비밀번호 변경 - 새 비밀번호 입력검사
    $("#nectarist_form_pwchange_new").on("input", function () {
        var inputpw = $("#nectarist_form_pwchange_new").val();

        if($("#nectarist_form_pwchange_pwchk").val() != ""){
            $("#nectarist_form_pwchange_pwchk").trigger("input");
        }
        
        $("#nectarist_button_pwchange").addClass("disabled");
        $(".nectarist_form_pw_result").addClass("d-none");
        $("#nectarist_form_pwchange_new").attr("data-valid", "N");
        $("#nectarist_form_pwchange_new").removeClass("invalid-input");

        if(/^[a-z0-9!@#$%^&*]*$/.test(inputpw) && inputpw.length >= 10 && inputpw.length <= 20) {
            $("#nectarist_form_pwchange_new").attr("data-valid", "Y");
            $("#nectarist_form_okpw").removeClass("d-none");
            if($("#nectarist_form_pwchange_pwchk").attr("data-valid") == "Y") {
                $("#nectarist_button_pwchange").removeClass("disabled");
            }
        }
        else {
            $("#nectarist_form_invalidpw").removeClass("d-none");
        }
    })

    // 비밀번호 변경 - 새 비밀번호 확인 입력검사
    $("#nectarist_form_pwchange_pwchk").on("input", function () {
        var inputpwchk = $("#nectarist_form_pwchange_pwchk").val();
        
        $("#nectarist_button_pwchange").addClass("disabled");
        $(".nectarist_form_pwchk_result").addClass("d-none");
        $("#nectarist_form_pwchange_pwchk").attr("data-valid", "N");
        $("#nectarist_form_pwchange_pwchk").removeClass("invalid-input");

        if(inputpwchk == $("#nectarist_form_pwchange_new").val()) {
            $("#nectarist_form_pwchange_pwchk").attr("data-valid", "Y");
            $("#nectarist_form_okpwchk").removeClass("d-none");
            if($("#nectarist_form_pwchange_new").attr("data-valid") == "Y") {
                $("#nectarist_button_pwchange").removeClass("disabled");
            }
        }
        else {
            $("#nectarist_form_invalidpwchk").removeClass("d-none");
        }
    })

    // 비밀번호 변경 - 비밀번호 변경요청
    function req_mypwchange(){
        if($("#nectarist_form_pwchange_new").attr("data-valid") == "Y" && $("#nectarist_form_pwchange_pwchk").attr("data-valid") == "Y"){
            var curpw = $("#nectarist_form_pwchange_cur").val();
            var newpw = $("#nectarist_form_pwchange_new").val();
            
            $.ajax({
                url: "/mypage_mypwchange/req_pwchange",
                data: {"curpw": curpw, "newpw": newpw},
                dataType: "json",
                success: function (result) {
                    if(result.is_valid_curpw == "Y"){
                        if(result.is_pw_changed == "Y"){
                            swal({
                                title: "비밀번호 변경 완료",
                                closeOnClickOutside: false,
                                closeOnEsc: false,
                                icon: "success",
                                button: "확인",
                            }).then((value) => {
                                location.reload();
                            });
                        }
                        else{
                            swal({
                                title: "비밀번호 변경 실패",
                                text: "관리자 문의 바랍니다.",
                                icon: "warning"
                            });
                        }
                    }
                    else {
                        swal({
                            title: "비밀번호 변경 실패",
                            text: "기존 비밀번호가 일치하지 않습니다.",
                            icon: "warning"
                        });
                    }
                }
            })
        }
    }
    
    // 마이페이지 권한 킥
    function req_mypagekick(){
        swal({
            title: "로그인 정보 없음",
            text: "로그인 후 이용 바랍니다.",
            closeOnClickOutside: false,
            closeOnEsc: false,
            icon: "warning",
            button: "확인",
        }).then((value) => {
            location.href = "/sign_in/";
        });
    }

// = = = = = = = = = = = = = = = = = = = = = = = = = = =
// 관리자
// = = = = = = = = = = = = = = = = = = = = = = = = = = =

    // 메인화면 설정 - 메인화면 게시글 삭제 저장
    var deleteMainBoard = [];
    $(function () {
        $(".nectarist-board .nectarist-board-check").on("click", function (e) {
            e.stopPropagation();
            if(!$(this).prop("checked")){
                deleteMainBoard.push($(this).attr("data-bno"));
            }
        });
    });

    // 메인화면 설정 - 메인화면 게시글 저장
    function req_setmain_save(){
        var selectedMainBoard = [];
        $(".nectarist-board .nectarist-board-check").each(function (idx, obj) {
            if($(obj).prop("checked")){
                selectedMainBoard.push($(obj).attr("data-bno"));
            }            
        });
        var saveSetmainData = {
            "selected": selectedMainBoard.join(','),
            "deleted": deleteMainBoard.join(',')
        }
        $.ajax({
            url: "/admin_asetmain/req_savesetmain",
            data: saveSetmainData,
            dataType: "json",
            success: function (result) {
                if(result.save_setmain_result == "Y"){
                    location.reload();
                }
                else {
                    swal({
                        title: "메인화면 설정 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })
    }

    // 칵테일 재료 관리 - 추가 팝업
    $("#nectarist_setingrdnt_addingrdnt").on("click", function () {
        $("#nectarist_setingrdnt_addmodal").modal("show");
    })

    // 칵테일 재료 관리 - 추가 팝업 - 재료 추가
    function req_setingrdnt_addingrdnt(btn){
        var ingObj = $(btn).prev(".ingrdnt-item")[0].outerHTML;
        $(ingObj).insertBefore(btn);

        // 버튼 활성화
        $("#nectarist_setingrdnt_addmodal .ingrdnt-item-del").prop("disabled", false);
    }

    // 칵테일 재료 관리 - 추가 팝업 - 재료 삭제
    $("#nectarist_setingrdnt_addmodal").on("click", ".ingrdnt-item-del", function () {
        $(this).parents(".ingrdnt-item").remove();

        // 한개인 경우 버튼 비활성화
        if($("#nectarist_setingrdnt_addmodal").find(".ingrdnt-item").length == 1){
            $("#nectarist_setingrdnt_addmodal .ingrdnt-item-del").prop("disabled", true);
        }
    })

    // 칵테일 재료 관리 - 추가 팝업 - 재료 저장
    function req_setingrdnt_addsave(){
        var ingList = [];
        $("#nectarist_setingrdnt_addmodal .ingrdnt-item").each(function () {
            var ingObj = {};
            ingObj["type"] = $(this).find("select").val();
            ingObj["name"] = $(this).find("input").val();
            ingList.push(ingObj);
        })
        $.ajax({
            url: "/admin_asetingrdnt/req_saveaddingrdnt",
            data: {"list": JSON.stringify(ingList)},
            dataType: "json",
            success: function (result) {
                if(result.save_result == "Y"){
                    location.href = "/admin_asetingrdnt/?page=1";
                }
                else {
                    swal({
                        title: "재료 추가 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })
    }

    // 칵테일 재료 관리 - 삭제 버튼
    $(".nectarist-setingrdnt-del").on("click", function () {
        swal({
            title: "재료 삭제",
            text: "해당 재료를 삭제합니다.",
            icon: "warning",           
            buttons: ["취소", "확인"]
        }).then((btnResult) => {
            if(btnResult){
                var ingNo = $(this).parents(".nectarist-ingrdnt-item").attr("data-ingrdnt-idx");
                $.ajax({
                    url: "/admin_asetingrdnt/req_delingrdnt",
                    data: {"ingno": ingNo},
                    dataType: "json",
                    success: function (result) {
                        if(result.save_result == "Y"){
                            location.reload();
                        }
                        else {
                            swal({
                                title: "재료 삭제 실패",
                                text: "잘못된 접근입니다.",
                                icon: "warning"
                            });
                        }
                    }
                })
            }
        });
    })

    // 칵테일 재료 관리 - 수정 팝업
    $(".nectarist-setingrdnt-mod").on("click", function () {
        var ingItem = $(this).parents(".nectarist-ingrdnt-item");
        var modModal = $("#nectarist_setingrdnt_modmodal");
        // 수정용 데이터 설정
        $(modModal).find("select").val($(ingItem).attr("data-ingrdnt-type"));
        $(modModal).find("input").val($(ingItem).attr("data-ingrdnt-name"));
        $(modModal).find(".ingrdnt-no").attr("data-ingrdnt-idx", $(ingItem).attr("data-ingrdnt-idx"));
        $("#nectarist_setingrdnt_modmodal").modal("show");
    })

    // 칵테일 재료 관리 - 수정 팝업 - 재료 저장
    function req_setingrdnt_modsave(){
        var ingObj = {};
        ingObj["type"] = $("#nectarist_setingrdnt_modmodal").find("select").val();
        ingObj["name"] = $("#nectarist_setingrdnt_modmodal").find("input").val();
        ingObj["no"] = $("#nectarist_setingrdnt_modmodal").find(".ingrdnt-no").attr("data-ingrdnt-idx");
        $.ajax({
            url: "/admin_asetingrdnt/req_savemodingrdnt",
            data: {"ing": JSON.stringify(ingObj)},
            dataType: "json",
            success: function (result) {
                if(result.save_result == "Y"){
                    location.reload();
                }
                else {
                    swal({
                        title: "재료 수정 실패",
                        text: "잘못된 접근입니다.",
                        icon: "warning"
                    });
                }
            }
        })
    }

    // 관리자 권한 킥
    function req_adminkick(){
        swal({
            title: "권한 없음",
            text: "접근 권한이 없습니다.",
            closeOnClickOutside: false,
            closeOnEsc: false,
            icon: "warning",
            button: "확인",
        }).then((value) => {
            location.href = "/";
        });
    }