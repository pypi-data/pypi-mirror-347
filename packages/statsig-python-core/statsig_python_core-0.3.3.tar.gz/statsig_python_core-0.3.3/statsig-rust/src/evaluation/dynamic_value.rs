use chrono::{DateTime, NaiveDateTime};
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use serde_json::{json, Value as JsonValue};
use std::collections::HashMap;

use super::dynamic_string::DynamicString;

#[macro_export]
macro_rules! dyn_value {
    ($x:expr) => {
        $crate::DynamicValue::from($x)
    };
}

#[derive(Debug, Clone, Default)]
pub struct DynamicValue {
    pub null: Option<()>,
    pub bool_value: Option<bool>,
    pub int_value: Option<i64>,
    pub float_value: Option<f64>,
    pub timestamp_value: Option<i64>,
    pub string_value: Option<DynamicString>,
    pub array_value: Option<Vec<DynamicValue>>,
    pub object_value: Option<HashMap<String, DynamicValue>>,
    pub json_value: JsonValue,
}

impl From<String> for DynamicValue {
    fn from(value: String) -> Self {
        let json_value = json!(value);
        let float_value = value.parse().ok();
        let int_value = value.parse().ok();

        let timestamp_value = Self::try_parse_timestamp(&value);

        DynamicValue {
            float_value,
            int_value,
            json_value,
            timestamp_value,
            string_value: Some(DynamicString::from(value)),
            ..Self::default()
        }
    }
}

impl From<&str> for DynamicValue {
    fn from(value: &str) -> Self {
        DynamicValue::from(value.to_string())
    }
}

impl From<usize> for DynamicValue {
    fn from(value: usize) -> Self {
        DynamicValue {
            json_value: json!(value),
            int_value: Some(value as i64),
            float_value: Some(value as f64),
            string_value: Some(DynamicString::from(value.to_string())),
            ..Self::default()
        }
    }
}

impl From<i64> for DynamicValue {
    fn from(value: i64) -> Self {
        DynamicValue {
            int_value: Some(value),
            float_value: Some(value as f64),
            string_value: Some(DynamicString::from(value.to_string())),
            json_value: json!(value),
            ..Self::default()
        }
    }
}

impl From<i32> for DynamicValue {
    fn from(value: i32) -> Self {
        Self::from(i64::from(value))
    }
}

impl From<f64> for DynamicValue {
    fn from(value: f64) -> Self {
        DynamicValue {
            int_value: Some(value as i64),
            float_value: Some(value),
            string_value: Some(DynamicString::from(value.to_string())),
            json_value: json!(value),
            ..Self::default()
        }
    }
}

impl From<bool> for DynamicValue {
    fn from(value: bool) -> Self {
        DynamicValue {
            bool_value: Some(value),
            string_value: Some(DynamicString::from(value.to_string())),
            json_value: json!(value),
            ..Self::default()
        }
    }
}

impl From<Vec<JsonValue>> for DynamicValue {
    fn from(value: Vec<JsonValue>) -> Self {
        DynamicValue::from(json!(value))
    }
}

impl From<JsonValue> for DynamicValue {
    fn from(value: JsonValue) -> Self {
        let json_value = value.clone();
        match value {
            JsonValue::Null => DynamicValue {
                null: Some(()),
                json_value,
                ..DynamicValue::new()
            },
            JsonValue::Bool(b) => DynamicValue {
                bool_value: Some(b),
                string_value: Some(DynamicString::from(b.to_string())),
                json_value,
                ..DynamicValue::new()
            },
            JsonValue::Number(n) => DynamicValue {
                float_value: n.as_f64(),
                int_value: n.as_i64(),
                string_value: Some(DynamicString::from(json_value.to_string())),
                json_value,
                ..DynamicValue::new()
            },
            JsonValue::String(s) => DynamicValue::from(s),
            JsonValue::Array(arr) => DynamicValue {
                array_value: Some(arr.into_iter().map(DynamicValue::from).collect()),
                string_value: Some(DynamicString::from(json_value.to_string())),
                json_value,
                ..DynamicValue::new()
            },
            JsonValue::Object(obj) => DynamicValue {
                object_value: Some(
                    obj.into_iter()
                        .map(|(k, v)| (k, DynamicValue::from(v)))
                        .collect(),
                ),
                json_value,
                ..DynamicValue::new()
            },
        }
    }
}

impl DynamicValue {
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }
    pub fn from<T: Into<DynamicValue>>(value: T) -> Self {
        value.into()
    }

    #[must_use]
    pub fn for_timestamp_evaluation(timestamp: i64) -> DynamicValue {
        DynamicValue {
            int_value: Some(timestamp),
            ..DynamicValue::default()
        }
    }

    fn try_parse_timestamp(s: &str) -> Option<i64> {
        if let Ok(ts) = s.parse::<i64>() {
            return Some(ts);
        }

        if let Ok(dt) = DateTime::parse_from_rfc3339(s) {
            return Some(dt.timestamp_millis());
        }

        if let Ok(ndt) = NaiveDateTime::parse_from_str(s, "%Y-%m-%d %H:%M:%S") {
            return Some(ndt.and_utc().timestamp_millis());
        }

        None
    }
}

impl PartialEq for DynamicValue {
    fn eq(&self, other: &Self) -> bool {
        self.null == other.null
            && self.bool_value == other.bool_value
            && self.int_value == other.int_value
            && self.float_value == other.float_value
            && self.string_value == other.string_value
            && self.array_value == other.array_value
            && self.object_value == other.object_value
    }
}

impl Serialize for DynamicValue {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        self.json_value.serialize(serializer)
    }
}

impl<'de> Deserialize<'de> for DynamicValue {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let json_value = JsonValue::deserialize(deserializer)?;
        Ok(DynamicValue::from(json_value))
    }
}
