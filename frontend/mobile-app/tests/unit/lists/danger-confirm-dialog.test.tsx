import { fireEvent, render, screen } from "@testing-library/react-native";
import { DangerConfirmDialog } from "../../../src/ui/DangerConfirmDialog";

describe("task 10 danger confirm dialog", () => {
  test("does not render when hidden", () => {
    render(
      <DangerConfirmDialog
        title="Delete list"
        message="Delete now"
        isVisible={false}
        confirmLabel="Delete list"
        onConfirm={async () => {}}
        onCancel={() => {}}
      />,
    );

    expect(screen.queryByText("Delete list")).toBeNull();
  });

  test("calls cancel and confirm handlers when visible", () => {
    const onCancel = jest.fn();
    const onConfirm = jest.fn(async () => {});

    render(
      <DangerConfirmDialog
        title="Delete list"
        message="Delete now"
        isVisible={true}
        confirmLabel="Delete list"
        onConfirm={onConfirm}
        onCancel={onCancel}
      />,
    );

    fireEvent.press(screen.getByLabelText("Cancel dangerous action"));
    fireEvent.press(screen.getByLabelText("Delete list"));

    expect(onCancel).toHaveBeenCalledTimes(1);
    expect(onConfirm).toHaveBeenCalledTimes(1);
  });

  test("disables actions while loading", () => {
    render(
      <DangerConfirmDialog
        title="Delete list"
        message="Delete now"
        isVisible={true}
        confirmLabel="Delete list"
        isLoading={true}
        onConfirm={async () => {}}
        onCancel={() => {}}
      />,
    );

    expect(screen.getByLabelText("Cancel dangerous action")).toBeDisabled();
    expect(screen.getByLabelText("Delete list")).toBeDisabled();
  });
});
