$("textarea").on("input", function () {
    $(this).height(0);
    $(this).height(this.scrollHeight);
});

if($("#nectarist_form_text").length > 0){
    CKEDITOR.replace("nectarist_form_text");
}

$(".select2").select2({dropdownParent: $("#container_center"), width: "100%"});

// select2 드롭다운 이슈 수정
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

/* = = = = = = = = = = = = = = = = = = = = = = = = = = =
 * 회원가입 
 * = = = = = = = = = = = = = = = = = = = = = = = = = = */
    // ID
    $("#nectarist_form_signup_id").on("input", function () {
        $(".nectarist_form_id_result").addClass("d-none");
        $("#nectarist_form_signup_id").attr("data-valid", "N");
        $("#nectarist_form_signup_id").removeClass("invalid-input");
    })
    function req_duplicate_id(){
        var inputid = $("#nectarist_form_signup_id").val();
        
        if(/^[a-z0-9]*$/.test(inputid) && inputid.length >= 6 && inputid.length <= 12) {
            $.ajax({
                url: "req_duplicate_id",
                data: {"inputid": inputid},
                dataType: "json",
                success: function (result) {
                    if(result.is_duplicate == "N") {
                        $("#nectarist_form_signup_id").attr("data-valid", "Y");
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

    // 비밀번호
    $("#nectarist_form_signup_pw").on("input", function () {
        var inputpw = $("#nectarist_form_signup_pw").val();
        
        $(".nectarist_form_pw_result").addClass("d-none");
        $("#nectarist_form_signup_id").attr("data-valid", "N");
        $("#nectarist_form_signup_pw").removeClass("invalid-input");

        if(/^[a-z0-9!@#$%^&*]*$/.test(inputpw) && inputpw.length >= 10 && inputpw.length <= 20) {
            $("#nectarist_form_signup_pw").attr("data-valid", "Y");
            $("#nectarist_form_okpw").removeClass("d-none");
        }
        else {
            $("#nectarist_form_invalidpw").removeClass("d-none");
        }
    })

    // 비밀번호 확인
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

    // 닉네임
    $("#nectarist_form_signup_name").on("input", function () {
        $(".nectarist_form_name_result").addClass("d-none");
        $("#nectarist_form_signup_name").attr("data-valid", "N");
        $("#nectarist_form_signup_name").removeClass("invalid-input");
    })
    function req_duplicate_name(){
        var inputname = $("#nectarist_form_signup_name").val();

        if(inputname.length >= 2 && inputname.length <= 10) {
            $.ajax({
                url: "req_duplicate_name",
                data: {"inputname": inputname},
                dataType: "json",
                success: function (result) {
                    if(result.is_duplicate == "N") {
                        $("#nectarist_form_signup_name").attr("data-valid", "Y");
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

    // 이메일
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

    // 회원가입
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
                url: "req_signup",
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
/* = = = = = = = = = = = = = = = = = = = = = = = = = = =
 * 로그인 
 * = = = = = = = = = = = = = = = = = = = = = = = = = = */
    // 로그인
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

    // 로그아웃
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
/* = = = = = = = = = = = = = = = = = = = = = = = = = = =
 * 댓글 
 * = = = = = = = = = = = = = = = = = = = = = = = = = = */
    // 칵테일 댓글 추가
    function req_add_cocktail_comment(cno) {
        var addCommentData = {
            "cno": cno,
            "text": $("#nectarist_comment_input").val()
        }
        $.ajax({
            url: "/req_add_cocktail_comment",
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
    // 게시글 댓글 추가
    function req_add_board_comment(bno) {
        var addCommentData = {
            "bno": bno,
            "text": $("#nectarist_comment_input").val()
        }
        $.ajax({
            url: "/req_add_board_comment",
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
/* = = = = = = = = = = = = = = = = = = = = = = = = = = =
 * 게시판
 * = = = = = = = = = = = = = = = = = = = = = = = = = = */
    // 게시글 추가
    function req_board_new(boardType, boardlink){
        var addBoardData = {
            "type": boardType,
            "title": $("#nectarist_form_title").val(),
            "text": CKEDITOR.instances.nectarist_form_text.getData(),
            "tag": $(".nectarist-form-select").val().join(',')
        }
        $.ajax({
            url: "/req_add_board",
            data: addBoardData,
            dataType: "json",
            success: function (result) {
                if(result.add_board_result == "Y"){
                    location.href = boardlink;
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
/* = = = = = = = = = = = = = = = = = = = = = = = = = = =
 * 냉장고 
 * = = = = = = = = = = = = = = = = = = = = = = = = = = */
    // 비어있는 경우
    if($("#nectarist_refrig_container .nectarist-ingrd-item").length == 0){
        $("#nectarist_ingrd_empty").removeClass("d-none");
    }
    // 재료 삭제 저장용
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
    // 하단 재료 냉장고에 넣기
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
    // 냉장고 저장
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
            url: "/req_save_refrig",
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
    // 냉장고 계산
    function req_refrig_calc(){
        var selectedIngrd = [];
        $("#nectarist_refrig_container .nectarist-ingrd-item").each(function (idx, obj) {
            selectedIngrd.push($(obj).attr("data-ingno"));
        });
        // 체크된 경우 저장
        if($("#nectarist_refrig_savechk").prop("checked")){
            var saveRefrigData = {
                "selected": selectedIngrd.join(','),
                "deleted": deleteIngrd.join(',')
            }
            $.ajax({
                url: "/req_save_refrig",
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