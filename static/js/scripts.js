var context = "/genshin_gacha_simulator";

$(document).ready(function () {
    // 입력 방식 변경 시 필드 토글 - Per Simulation
    $("input[name='input_method']").change(function () {
        if ($(this).val() === 'pulls') {
            $("#pulls_input_field").show();
            $("#gemstones_input_field").hide();
            $("#gemstones_per_simulation").val('0');
            $("#gemstones_per_simulation").removeAttr('required');
            $("#pulls_per_simulation").attr('required', 'required');
        } else {
            $("#pulls_input_field").hide();
            $("#gemstones_input_field").show();
            $("#pulls_per_simulation").val('0');
            $("#pulls_per_simulation").removeAttr('required');
            $("#gemstones_per_simulation").attr('required', 'required');
        }
    });

    // 입력 방식 변경 시 필드 토글 - Gacha Simulation
    $("input[name='input_method_gacha']").change(function () {
        if ($(this).val() === 'pulls') {
            $("#pulls_input_field_gacha").show();
            $("#gemstones_input_field_gacha").hide();
            $("#gemstones_gacha").val('0');
            $("#gemstones_gacha").removeAttr('required');
            $("#pulls_gacha").attr('required', 'required');
        } else {
            $("#pulls_input_field_gacha").hide();
            $("#gemstones_input_field_gacha").show();
            $("#pulls_gacha").val('0');
            $("#pulls_gacha").removeAttr('required');
            $("#gemstones_gacha").attr('required', 'required');
        }
    });

    // Gacha Simulation AJAX
    $("#start-gacha").click(function () {
        var gacha_type = $("#gacha_type").val();
        var pulls;

        var input_method_gacha = $("input[name='input_method_gacha']:checked").val();

        if (input_method_gacha === 'pulls') {
            pulls = $("#pulls_gacha").val();
        } else {
            var gemstones = $("#gemstones_gacha").val();
            pulls = Math.floor(gemstones / 160);
        }

        if (pulls < 1) {
            alert("원석이 부족하여 최소 1 가챠를 할 수 없습니다.");
            return;
        }

        var pulls_int = parseInt(pulls);
        var target_character = parseInt($("#target_character").val());
        var target_weapon = parseInt($("#target_weapon").val());

        // 입력 값 유효성 검사
        if (isNaN(pulls_int) || pulls_int <= 0) {
            alert("가챠 횟수는 1 이상이어야 합니다.");
            return;
        }
        if (isNaN(target_character) || isNaN(target_weapon)) {
            alert("목표 캐릭터 수와 목표 무기 수는 숫자여야 합니다.");
            return;
        }
        if (target_character < 0) {
            alert("목표 캐릭터 수는 0 이상이어야 합니다.");
            return;
        }
        if (target_weapon < 0) {
            alert("목표 무기 수는 0 이상이어야 합니다.");
            return;
        }
        if (target_character === 0 && target_weapon === 0) {
            alert("목표 캐릭터 수와 목표 무기 수 중 최소 하나는 1 이상이어야 합니다.");
            return;
        }

        // 버튼 클릭 시 스타일링 효과 추가
        $("#start-gacha").prop("disabled", true).removeClass("btn-primary").addClass("btn-success").text("진행 중...");

        $.ajax({
            url: context + "/gacha/simulate",
            type: "POST",
            data: { gacha_type: gacha_type, pulls: pulls_int },
            success: function (response) {
                if (response.error) {
                    $("#stats_gacha").text(response.error);
                    $("#result_gacha").text("");
                } else {
                    $("#stats_gacha").hide().html(response.stats).fadeIn(800);
                    $("#result_gacha").hide().html(response.details).fadeIn(800);
                }
                $("#start-gacha").prop("disabled", false).removeClass("btn-success").addClass("btn-primary").text("시뮬레이션 시작");
            },
            error: function (xhr) {
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    $("#stats_gacha").text(xhr.responseJSON.error);
                } else {
                    $("#stats_gacha").text("오류가 발생했습니다. 입력 값을 확인하세요.");
                }
                $("#result_gacha").text("");
                $("#start-gacha").prop("disabled", false).removeClass("btn-success").addClass("btn-primary").text("시뮬레이션 시작");
            }
        });
    });

    // Per Simulation AJAX
    $("#start-per_simulation").click(function () {
        var pulls;
        var input_method = $("input[name='input_method']:checked").val();

        if (input_method === 'pulls') {
            pulls = $("#pulls_per_simulation").val();
        } else {
            var gemstones = $("#gemstones_per_simulation").val();
            // 원석을 가챠 수로 변환 (160 원석 = 1 가챠, 소수점 버림)
            pulls = Math.floor(gemstones / 160);
        }
        if (pulls < 1) {
            alert("원석이 부족하여 최소 1 가챠를 할 수 없습니다.");
            return;
        }

        var pulls_int = parseInt(pulls);
        var target_character = parseInt($("#target_character").val());
        var target_weapon = parseInt($("#target_weapon").val());

        // 입력 값 유효성 검사
        if (isNaN(pulls_int) || pulls_int <= 0) {
            alert("가챠 횟수는 1 이상이어야 합니다.");
            return;
        }
        if (isNaN(target_character) || isNaN(target_weapon)) {
            alert("목표 캐릭터 수와 목표 무기 수는 숫자여야 합니다.");
            return;
        }
        if (target_character < 0) {
            alert("목표 캐릭터 수는 0 이상이어야 합니다.");
            return;
        }
        if (target_weapon < 0) {
            alert("목표 무기 수는 0 이상이어야 합니다.");
            return;
        }
        if (target_character === 0 && target_weapon === 0) {
            alert("목표 캐릭터 수와 목표 무기 수 중 최소 하나는 1 이상이어야 합니다.");
            return;
        }

        // 버튼 클릭 시 스타일링 효과 추가
        $("#start-per_simulation").prop("disabled", true).removeClass("btn-primary").addClass("btn-success").text("진행 중...");

        $.ajax({
            url: context + "/per_simulation/simulate",
            type: "POST",
            data: { pulls: pulls_int, target_character: target_character, target_weapon: target_weapon },
            success: function (response) {
                if (response.error) {
                    $("#result_per_simulation").text(response.error);
                } else {
                    $("#result_per_simulation").hide().html(`목표 ${target_character} 캐릭터와 ${target_weapon} 무기를 획득할 확률: ${(response.probability * 100).toFixed(2)}%`).fadeIn(800);
                }
                $("#start-per_simulation").prop("disabled", false).removeClass("btn-success").addClass("btn-primary").text("시뮬레이션 시작");
            },
            error: function (xhr) {
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    $("#result_per_simulation").text(xhr.responseJSON.error);
                } else {
                    $("#result_per_simulation").text("오류가 발생했습니다. 입력 값을 확인하세요.");
                }
                $("#start-per_simulation").prop("disabled", false).removeClass("btn-success").addClass("btn-primary").text("시뮬레이션 시작");
            }
        });
    });
});
