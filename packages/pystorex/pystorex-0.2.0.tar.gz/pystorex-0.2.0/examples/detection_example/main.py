import json
from pathlib import Path
import sys
from reactivex import operators as ops

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import time
from fence.fence_effects import FenceEffects
from helmet.helmet_effects import HelmetEffects
from shared.detection_store import store
from shared.utils import create_sample_data
from shared.detection_actions import visual_recognition
from helmet.helmet_selectors import get_violation_persons
from fence.fence_selectors import get_intrusion_persons
from pystorex.store_selectors import create_selector

from pystorex.immutable_utils import to_dict
from helmet.helmet_reducer import helmet_status_reducer
from fence.fence_reducer import fence_status_reducer

store.register_root(
    {
        "helmet_status": helmet_status_reducer,
        "fence_status": fence_status_reducer
    }
)

store.register_effects(
    HelmetEffects,
    FenceEffects
)
get_helmet_status_state = lambda state: state["helmet_status"]
get_fence_status_state = lambda state: state["fence_status"]
get_helmet_states = create_selector(
    get_helmet_status_state, result_fn=lambda state: state.get('helmet_states',{})
)
get_fence_states = create_selector(
    get_fence_status_state, result_fn=lambda state: state.get('fence_states',{})
)
if __name__ == "__main__":
    store._action_subject.subscribe(
        on_next=lambda action: print(
            f"分發動作: {action.type} - 负载: {action.payload}"
        )
    )
    # 訂閱違規狀態的人員
    # store.select(get_violation_persons).subscribe(
    #     on_next=lambda violations_tuple: (
    #         print(f"違規人員變化: {len(violations_tuple[1])} 人\n")
    #         if violations_tuple[1]
    #         else None
    #     )
    # )

    # # 訂閱闖入禁區的人員
    # store.select(get_intrusion_persons).subscribe(
    #     on_next=lambda intrusions_tuple: (
    #         print(f"闖入禁區人員變化: {len(intrusions_tuple[1])} 人\n")
    #         if intrusions_tuple[1]
    #         else None
    #     )
    # )
    # # 訂閱並打印完整狀態
    store.select(get_helmet_states).subscribe(
        on_next=lambda tpl: print(
            "人員安全帽狀態變化:\n"
            + json.dumps(to_dict(tpl[1]), ensure_ascii=False, indent=2)
            + "\n"
        )
    )
    store.select(get_fence_states).pipe(
        # ops.filter(lambda fence_states: fence_states is not None),
        ).subscribe(
        on_next=lambda tpl: print(
            "人員禁區狀態變化:\n"
            + json.dumps(
                # 如果需要序列化 pydantic model，可先轉 dict
                {pid: to_dict(pstate) for pid, pstate in tpl[1].items()},
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
    )

    # 生成模擬數據
    sample_data = create_sample_data()

    # 模擬視覺識別事件
    print("\n==== 開始模擬視覺識別事件 ====")
    for i, frame_data in enumerate(sample_data):
        print(f"\n=== 第 {i+1} 幀 ===")
        print(
            f"識別結果: 人數 {len(frame_data['persons'])}, 安全帽數 {len(frame_data['helmets'])}"
        )

        # 只分發視覺識別Action
        store.dispatch(visual_recognition(frame_data))

        # 暫停以便觀察
        time.sleep(1)

    print("\n==== 模擬結束 ====")
    print(store.state)
